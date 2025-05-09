import os
import time
import numpy as np
import hydra
import torch
import subprocess
import logging
import pandas as pd
import shutil
from datetime import datetime
from biotite.sequence.io import fasta
import GPUtil
from typing import Optional, Union, List
from analysis import utils as au
from analysis import metrics
from data import utils as du
from omegaconf import DictConfig, OmegaConf
from openfold.data import data_transforms
import esm
from pathlib import Path
import mdtraj as md
from openfold.np import residue_constants
from tmtools import tm_align
from openfold.utils.superimposition import superimpose
from tqdm import tqdm
import re


class EvalRunner:

    def __init__(
        self,
        conf: DictConfig,
    ):

        self._log = logging.getLogger(__name__)
        self._conf = conf

        # Set random seed
        self._rng = np.random.default_rng(self._conf.seed)

        # Set model hub directory for ESMFold.
        torch.hub.set_dir(self._conf.pt_hub_dir)

        # Set-up accelerator
        if torch.cuda.is_available():
            available_gpus = "".join(
                [str(x) for x in GPUtil.getAvailable(order="memory", limit=8)]
            )
            self.device = f"cuda:{available_gpus[0]}"
        else:
            self.device = "cpu"

        self._log.info(f"Using device: {self.device}")

        self._pmpnn_dir = self._conf.pmpnn_dir
        self._foldseek_database = self._conf.foldseek_database

        # Load ESMFold model
        # self._folding_model = esm.pretrained.esmfold_v0().eval()
        # self._folding_model = self._folding_model.to(self.device)

        version = "1"  # @param ["0", "1"]
        self.model_name = "esmfold_v0.model" if version == "0" else "esmfold.model"
        import os, time

        if not os.path.isfile(self.model_name):
            # download esmfold params
            #   os.system("apt-get install aria2 -qq")
            os.system(
                f"aria2c -q -x 16 https://colabfold.steineggerlab.workers.dev/esm/{self.model_name} &"
            )

            if not os.path.isfile("finished_install"):
                # install libs
                print("installing libs...")
                os.system(
                    "pip install -q omegaconf pytorch_lightning biopython ml_collections einops py3Dmol modelcif"
                )
                os.system("pip install -q git+https://github.com/NVIDIA/dllogger.git")

                print("installing openfold...")
                # install openfold
                os.system(
                    f"pip install -q git+https://github.com/sokrypton/openfold.git"
                )

                print("installing esmfold...")
                # install esmfold
                os.system(f"pip install -q git+https://github.com/sokrypton/esm.git")
                os.system("touch finished_install")

            # wait for Params to finish downloading...
            while not os.path.isfile(self.model_name):
                time.sleep(5)
            if os.path.isfile(f"{self.model_name}.aria2"):
                print("downloading params...")
            while os.path.isfile(f"{self.model_name}.aria2"):
                time.sleep(5)

    def _calc_bb_rmsd(self, mask, sample_bb_pos, folded_bb_pos):
        aligned_rmsd = superimpose(
            torch.tensor(sample_bb_pos),
            torch.tensor(folded_bb_pos),
            mask.unsqueeze(1).repeat(1, 3).T,
        )
        return aligned_rmsd[1].item()

    def calc_tm_score(self, pos_1, pos_2, seq_1, seq_2):
        tm_results = tm_align(pos_1, pos_2, seq_1, seq_2)
        return tm_results.tm_norm_chain1, tm_results.tm_norm_chain2

    def pdbTM(
        self,
        input: Union[str, Path] = None,
        process_id: int = 0,
        save_tmp: bool = False,
        foldseek_path: Optional[Union[Path, str]] = None,
    ) -> Union[float, dict]:
        """
        Calculate pdbTM values with a customized set of parameters by Foldseek.

        Args:
        `input`: Input PDB file or csv file containing PDB paths.
        `process_id`: Used for saving temporary files generated by Foldseek.
        `save_tmp`: If True, save tmp files generated by Foldseek, otherwise deleted after calculation.
        `foldseek_path`: Path of Foldseek binary file for executing the calculations.
                        If you've already installed Foldseek through conda, just use "foldseek"
                        instead of this path.

        CMD args:
        `pdb100`: Path of PDB database created compatible with Foldseek format.
        `output_file`: .m8 file containing Foldseek search results. Deleted if `save_tmp` = False.
        `tmp`: Temporary path when running Foldseek.
        For other CMD parameters and usage, we suggest users go to Foldseek official website
        (https://github.com/steineggerlab/foldseek) or type `foldseek easy-search -h` for detailed information.

        Returns:
        `top_pdbTM`: The highest pdbTM value among the top three targets hit by Foldseek.
        """
        foldseek_database_path = self._foldseek_database

        # Handling multiprocessing
        base_tmp_path = "./tmp/"
        tmp_path = os.path.join(base_tmp_path, f"process_{process_id}")
        os.makedirs(tmp_path, exist_ok=True)

        # Check whether input is a directory or a single file
        if ".pdb" in input:
            output_file = f"./{os.path.basename(input)}_{process_id}.m8"

            cmd = f"foldseek easy-search \
                    {input} \
                    {foldseek_database_path} \
                    {output_file} \
                    {tmp_path} \
                    --format-mode 4 \
                    --format-output query,target,evalue,alntmscore,rmsd,prob \
                    --alignment-type 1 \
                    --num-iterations 2 \
                    -e inf \
                    -v 0"

            if foldseek_path is not None:
                cmd.replace("foldseek", {foldseek_path})

            _ = subprocess.run(
                cmd,
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            result = pd.read_csv(output_file, sep="\t")
            top_pdbTM = round(result["alntmscore"].head(1).max(), 3)

            if save_tmp == False:
                os.remove(output_file)

        else:
            return None

        return top_pdbTM

    def calc_mdtraj_metrics(self, pdb_path: str):
        try:
            traj = md.load(pdb_path)
            pdb_ss = md.compute_dssp(traj, simplified=True)
            pdb_coil_percent = np.mean(pdb_ss == "C")
            pdb_helix_percent = np.mean(pdb_ss == "H")
            pdb_strand_percent = np.mean(pdb_ss == "E")
            pdb_ss_percent = pdb_helix_percent + pdb_strand_percent
            pdb_rg = md.compute_rg(traj)[0]
        except IndexError as e:
            print("Error in calc_mdtraj_metrics: {}".format(e))
            pdb_ss_percent = 0.0
            pdb_coil_percent = 0.0
            pdb_helix_percent = 0.0
            pdb_strand_percent = 0.0
            pdb_rg = 0.0
        return {
            "non_coil_percent": pdb_ss_percent,
            "coil_percent": pdb_coil_percent,  # coil
            "helix_percent": pdb_helix_percent,  # alpha helix
            "strand_percent": pdb_strand_percent,  # beta sheet
            "radius_of_gyration": pdb_rg,
        }

    def run_max_cluster(self, designable_file_path, designable_dir):
        pmpnn_args = [
            "./maxcluster64bit",
            "-l",
            designable_file_path,
            os.path.join(designable_dir, "all_by_all_lite"),
            "-C",
            "2",
            "-in",
            "-Rl",
            os.path.join(designable_dir, "tm_results.txt"),
            "-Tm",
            "0.5",
        ]
        process = subprocess.Popen(
            pmpnn_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, _ = process.communicate()

        # Extract number of clusters
        match = re.search(
            r"INFO\s*:\s*(\d+)\s+Clusters\s+@\s+Threshold\s+(\d+\.\d+)\s+\(\d+\.\d+\)",
            stdout.decode("utf-8"),
        )
        clusters = int(match.group(1))
        cluster_results_path = os.path.join(designable_dir, "cluster_results.txt")
        with open(cluster_results_path, "w") as f:
            f.write(stdout.decode("utf-8"))

        # Extract cluster centroids
        cluster_lines = stdout.decode("utf-8").split("\n")
        centroid_section = False
        for line in cluster_lines:
            if "Centroids" in line:
                centroid_section = True
            if centroid_section:
                match = re.search(r"(?<=\s)(\/[^\s]+\.pdb)", line)
                if match is not None:
                    centroid_path = match.group(1)
                    copy_name = centroid_path.split("/")[-2] + ".pdb"
                    shutil.copy(centroid_path, os.path.join(designable_dir, copy_name))
        return clusters

    def calc_designability(
        self,
        decoy_pdb_dir: str,
        reference_pdb_path: str,
    ):
        """Run self-consistency on design proteins against reference protein.

        Args:
            decoy_pdb_dir: directory where designed protein files are stored.
            reference_pdb_path: path to reference protein file

        Returns:
            Writes ProteinMPNN outputs to decoy_pdb_dir/seqs
            Writes ESMFold outputs to decoy_pdb_dir/esmf
            Writes results in decoy_pdb_dir/sc_results.csv
        """

        # Run PorteinMPNN
        output_path = os.path.join(decoy_pdb_dir, "parsed_pdbs.jsonl")
        process = subprocess.Popen(
            [
                "python",
                f"{self._pmpnn_dir}/helper_scripts/parse_multiple_chains.py",
                f"--input_path={reference_pdb_path}",
                f"--output_path={output_path}",
            ]
        )
        _ = process.wait()
        num_tries = 0
        ret = -1
        pmpnn_args = [
            "python",
            f"{self._pmpnn_dir}/protein_mpnn_run.py",
            "--out_folder",
            decoy_pdb_dir,
            "--jsonl_path",
            output_path,
            "--num_seq_per_target",
            "3",
            "--sampling_temp",
            "0.1",
            "--seed",
            "38",
            "--batch_size",
            "1",
        ]

        while ret < 0:
            try:
                process = subprocess.Popen(
                    pmpnn_args, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
                )
                ret = process.wait()
            except Exception as e:
                num_tries += 1
                self._log.info(f"Failed ProteinMPNN. Attempt {num_tries}/5")
                torch.cuda.empty_cache()
                if num_tries > 4:
                    raise e
        mpnn_fasta_path = os.path.join(decoy_pdb_dir, "seqs", "sample.fa")

        # Run ESMFold on each ProteinMPNN sequence and calculate metrics.
        mpnn_results = {
            "tm_score": [],
            "bb_rmsd": [],
            "sample_path": [],
            "header": [],
            "sequence": [],
            "ptm": [],
            "plddt": [],
            "pae": [],
        }

        esmf_dir = os.path.join(decoy_pdb_dir, "esmf")
        os.makedirs(esmf_dir, exist_ok=True)
        fasta_seqs = fasta.FastaFile.read(mpnn_fasta_path)
        sample_feats = du.parse_pdb_feats(
            "sample.pdb", os.path.join(reference_pdb_path, "sample.pdb")
        )
        for i, (header, string) in enumerate(fasta_seqs.items()):

            if i == 0:
                continue
            
            # Run ESMFold
            esmf_sample_path = os.path.join(esmf_dir, f"sample_{i}.pdb")
            # _ = self.run_folding(string, esmf_sample_path)
            ptm, plddt, pae = self.run_folding(string, esmf_sample_path)
            
            esmf_feats = du.parse_pdb_feats("folded_sample", esmf_sample_path)
            sample_seq = du.aatype_to_seq(sample_feats["aatype"])

            # Calculate scTM of ESMFold outputs with reference protein
            _, tm_score = self.calc_tm_score(
                sample_feats["bb_positions"],
                esmf_feats["bb_positions"],
                sample_seq,
                sample_seq,
            )

            res_mask = torch.ones(sample_feats["bb_positions"].shape[0])

            # print(res_mask.shape)
            # print(sample_feats["bb_positions"].shape)
            # print(esmf_feats["bb_positions"].shape)

            bb_rmsd = self._calc_bb_rmsd(
                res_mask, sample_feats["bb_positions"], esmf_feats["bb_positions"]
            )

            mpnn_results["tm_score"].append(tm_score)
            mpnn_results["bb_rmsd"].append(bb_rmsd)
            mpnn_results["sample_path"].append(esmf_sample_path)
            mpnn_results["header"].append(header)
            mpnn_results["sequence"].append(string)
            mpnn_results["ptm"].append(ptm)
            mpnn_results["plddt"].append(plddt)
            mpnn_results["pae"].append(pae)

        # Save results to CSV
        csv_path = os.path.join(decoy_pdb_dir, "sc_results.csv")
        # print(mpnn_results)
        mpnn_results = pd.DataFrame(mpnn_results)
        mpnn_results.to_csv(csv_path)

        return mpnn_results

    def calc_all_metrics(
        self,
        decoy_pdb_dir: str,
        reference_pdb_path: str,
    ):

        print("Calculating all metrics...")
        print(
            "##########################################################################"
        )
        print("Calculating designability...")
        # calc self-consistency results
        sc_results = self.calc_designability(decoy_pdb_dir, reference_pdb_path)
        print(sc_results)
        print(
            "##########################################################################"
        )
        print("Calculating substructure ratio...")
        # calc substructure ratio
        pdb_path = os.path.join(reference_pdb_path, "sample.pdb")
        calc_ratio = self.calc_mdtraj_metrics(pdb_path)
        # save to csv, for debugging
        df = pd.DataFrame(calc_ratio, index=[0])
        print(df)
        print(
            "##########################################################################"
        )
        print("Calculating novelty (pdbTM)...")
        # calculate novelty (pdbTM)
        value = self.pdbTM(pdb_path, 1)
        print(
            f"TM-Score between {os.path.basename(pdb_path)} and its closest protein in PDB is {value}."
        )
        print(
            "##########################################################################"
        )

    # def run_folding(self, sequence, save_path):
    #     """Run ESMFold on sequence."""
    #     with torch.no_grad():
    #         output = self._folding_model.infer_pdb(sequence)

    #     with open(save_path, "w") as f:
    #         f.write(output)
    #     return output

    def run_folding(self, sequence, save_path):

        from string import ascii_uppercase, ascii_lowercase
        import hashlib, re, os
        import numpy as np
        import torch
        from jax.tree_util import tree_map
        import matplotlib.pyplot as plt
        from scipy.special import softmax
        import gc

        def parse_output(output):
            pae = (output["aligned_confidence_probs"][0] * np.arange(64)).mean(-1) * 31
            plddt = output["plddt"][0, :, 1]

            bins = np.append(0, np.linspace(2.3125, 21.6875, 63))
            sm_contacts = softmax(output["distogram_logits"], -1)[0]
            sm_contacts = sm_contacts[..., bins < 8].sum(-1)
            xyz = output["positions"][-1, 0, :, 1]
            mask = output["atom37_atom_exists"][0, :, 1] == 1
            o = {
                "pae": pae[mask, :][:, mask],
                "plddt": plddt[mask],
                "sm_contacts": sm_contacts[mask, :][:, mask],
                "xyz": xyz[mask],
            }
            return o

        def get_hash(x):
            return hashlib.sha1(x.encode()).hexdigest()

        alphabet_list = list(ascii_uppercase + ascii_lowercase)

        jobname = "test"  # @param {type:"string"}
        jobname = re.sub(r"\W+", "", jobname)[:50]

        # sequence = "GWSTELEKHREELKEFLKKEGITNVEIRIDNGRLEVRVEGGTERLKRFLEELRQKLEKKGYTVDIKIE" #@param {type:"string"}
        sequence = re.sub("[^A-Z:]", "", sequence.replace("/", ":").upper())
        sequence = re.sub(":+", ":", sequence)
        sequence = re.sub("^[:]+", "", sequence)
        sequence = re.sub("[:]+$", "", sequence)
        copies = 1  # @param {type:"integer"}
        if copies == "" or copies <= 0:
            copies = 1
        sequence = ":".join([sequence] * copies)
        num_recycles = 3  # @param ["0", "1", "2", "3", "6", "12", "24"] {type:"raw"}
        chain_linker = 25

        ID = jobname + "_" + get_hash(sequence)[:5]
        seqs = sequence.split(":")
        lengths = [len(s) for s in seqs]
        length = sum(lengths)
        # print("length", length)

        u_seqs = list(set(seqs))
        if len(seqs) == 1:
            mode = "mono"
        elif len(u_seqs) == 1:
            mode = "homo"
        else:
            mode = "hetero"

        if "model" not in dir() or self.model_name != model_name_:
            if "model" in dir():
                # delete old model from memory
                del model
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()

            # Warning: this will overwrite the default dtype
            torch.set_default_dtype(torch.float32)
            model = torch.load(self.model_name, weights_only=False)
            model.eval().cuda().requires_grad_(False)
            model_name_ = self.model_name

        # optimized for Tesla T4
        if length > 700:
            model.set_chunk_size(64)
        else:
            model.set_chunk_size(128)

        torch.cuda.empty_cache()
        output = model.infer(
            sequence,
            num_recycles=num_recycles,
            chain_linker="X" * chain_linker,
            residue_index_offset=512,
        )

        pdb_str = model.output_to_pdb(output)[0]
        output = tree_map(lambda x: x.cpu().numpy(), output)
        ptm = output["ptm"][0]
        plddt = output["plddt"][0, ..., 1].mean()
        O = parse_output(output)
        # print(f"ptm: {ptm:.3f} plddt: {plddt:.3f}")
        # os.system(f"mkdir -p {ID}")
        # prefix = f"{ID}/ptm{ptm:.3f}_r{num_recycles}_default"
        # np.savetxt(f"{prefix}.pae.txt", O["pae"], "%.3f")
        
        with open(save_path, "w") as out:
            out.write(pdb_str)

        return ptm, plddt, O["pae"].mean()
        
    def calc_diversity(self, pdb_csv_path):
        """Get diversity from csv file.

        pdb_csv_path : str
            Path to the csv file containing the pdb paths
        """

        df = pd.read_csv(pdb_csv_path, header=None)

        pdb_path_list = df[0].tolist()

        # log_msg("Running clustering")
        cluster_dir = os.path.join(Path(pdb_csv_path).parent, "cluster")
        os.makedirs(cluster_dir, exist_ok=True)
        # all_metrics = pd.read_csv(metric_path)
        designable_paths = pdb_path_list
        designable_file_path = os.path.join(cluster_dir, "designable_paths.txt")
        with open(designable_file_path, "w") as f:
            f.write("\n".join(designable_paths))

        clusters = self.run_max_cluster(designable_file_path, cluster_dir)

        return clusters


@hydra.main(version_base=None, config_path="configs", config_name="evaluation")
def run(conf: DictConfig) -> None:

    # Example pdb path
    pdb_path = "/home/shuaikes/server2/shuaikes/projects/protein-evaluation-notebook/example_data/length_70/sample_0/"
    sc_output_dir = os.path.join(pdb_path, "self_consistency")
    os.makedirs(sc_output_dir, exist_ok=True)

    # run reward model
    EvalModel = EvalRunner(conf)
    EvalModel.calc_all_metrics(sc_output_dir, pdb_path)

    pdb_csv_path = "/home/shuaikes/server2/shuaikes/projects/protein-evaluation-notebook/pdb_path.csv"
    # clusters = EvalModel.calc_diversity(pdb_csv_path)


if __name__ == "__main__":
    run()
