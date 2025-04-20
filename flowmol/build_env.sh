#!/bin/bash
set -e # this will stop the script on first error

# get the name of the current conda environment
ENV_NAME=$(basename "$CONDA_PREFIX")

# print the name of the current conda environment to the terminal
echo "Building flowmol into the environment '$ENV_NAME'"

conda install pytorch=2.2.0 pytorch-cuda=12.1 -c pytorch -c nvidia -y
conda install pytorch-cluster=1.6.3 pytorch-scatter=2.1.2=py311_torch_2.2.0_cu121 -c pyg -y
conda install -c dglteam/label/cu121 dgl=2.0.0.cu121=py311_0 -y
conda install -c conda-forge pytorch-lightning=2.1.3=pyhd8ed1ab_0 -y
conda install -c conda-forge rdkit=2023.09.4 pystow einops -y

pip install wandb useful_rdkit_utils py3Dmol --no-input
pip install -e ./