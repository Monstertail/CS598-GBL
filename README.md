# CS598-GBL - Gen Mod for BioMed &amp; Life Sci

### Course Console

**Lectures**: 0220 Siebel Center for Computer Science, MW: 9:30 AM – 10:45 AM

| **Member (NetID)** | **Role** | **Office Hours** |
| --- | --- | --- |
| Ge Liu (geliu) | Instructor | Mon 3:00-4:00 SC3212 |
| Yanru Qu (yanruqu2) | TA | Mon 11-12 SC 3rd floor near elevator |

**Canvas**: https://canvas.illinois.edu/courses/56424

- For homework/report submission
- For open discussion

**Github (Course website)**: https://github.com/gelab-uiuc/CS598-GBL

- Covering most of the course information, including schedule and reading lists

**Note**: Please use **Canvas Discussion** to submit your course-related questions. Please **DO NOT** email the TA or Prof. Liu directly, unless the matter is private or only concerns yourself.

### Course Description

In this course, we will discuss recent advances in generative AI for biomedicine, with a special focus on geometric-aware deep learning, multimodal diffusion/flow matching on diverse data manifolds, and language models. We will also discuss foundational models for biomedicine and life sciences applications such as protein design, drug discovery, and understanding the functions and dynamics of complex biomolecular systems.

**Learning Objectives:** This course will introduce generative model basics, their application in biomedicines, and other impactful research works. At the end of this course, you will be able to:

- Have a good overview and basic knowledge of state-of-the-art generative models in biomedicines & life science
- Familiar with the research process: proposal, presentation, paper writing, review & rebuttal, hands-on experiments
- Have critical thinking and assessment of research papers

**Structure**: This will be a graduate-level course in seminar format.

- 6 instructor lectures: we will first review the biology & generative model basics. See schedule
- 1 project brain-storm session
- 15 paper-reading lectures: we will select 15 research sub-topics and reading lists for students to read, present, and discuss, covering the following topics:
    - Language models for biomedicine
    - Generative models for chemical molecules
    - Generative models for protein folding and design
    - Complex-based design with generative models: Structure-based drug design, peptide, antibody, enzyme, and molecular docking
    - RLHF/conditional generation/Guidance
- mid-term and final presentations

### Grading Policy

**Groups**: All activities of this course, except your attendance, will be performed in groups of 3 students, in a total of 15 groups. **By Feb 3**, most groups should submit their memberships (**exactly 3**) and topic preference (see 5 general topics in **Structure**). For students who do not find a group, we will assign groups according to their topic preference.

| **Component** | **Weight** | **Breakdown** |
| --- | --- | --- |
| Pre-class Reading | 10% | 10 pt 15 lectures |
| In-class Discussion | 30% | - 10% Presentation - 10% Rebuttal - 10% Review |
| Hands-on Experiments | 20% | - 10% Scripts & Generation Results - 10% Report |
| Final Project | 40% | - 5% Proposal - 15% Final Presentation - 20% Final Report |

**Pre-class Reading**

- Group Assignment: Each paper-reading lecture will have several required readings and optional related readings.  Each group should read at least one of the papers and submit at least 1 insightful question or idea related to the paper you read here https://docs.google.com/spreadsheets/d/1Q-wPi2Ezbv0QJe8hN2tBNC15WmkPaquhuJqkT4p5bWk/edit?usp=sharing before the lecture.

**In-class Discussion**

- In each paper-reading lecture, 2 groups will be signed up as the main leaders of the discussion, with each group playing one of the 2 roles: **presenters** or **reviewers**. These 2 groups are required to submit assignments (see below). Other groups are encouraged to participate in class discussions. Throughout the semester, each group needs to sign up for each one of the roles once, totaling participation in 2 different subtopics.
- Group Assignment for designated presenters and reviewers:
    - For presenter: submit slides (at least 20 pages) for all required readings **before the lecture,** and present the papers **during the class (45 min presentation);** submit a rebuttal **within 6 days after the lecture**
    - For reviewers: submit academic reviews about required readings by **EOD of the lecture**

**Hands-on Experiments**

We’ll release 1-3 benchmark challenges during the semester. Each group should choose 1 challenge and use its codebase to generate results and evaluation metrics, and finish a short report like the experiment section in a paper. The report should cover experiment settings and results analysis. Each group should submit the experiment reports 2 weeks **before the final presentation (Apr 23).**

**Final Project**

Each group should complete a final project in one of the following types:

1. Comprehensive literature survey on one advanced subtopic in generative AI for biomedicine (doesn't need to be one of the subtopics of the lecture, but should be related to the topics of the class).
2. Benchmarking & dataset paper (opportunity to submit to Neurips Benchmark track)
3. Open-ended research (opportunity to submit to Neurips main track)

Each group should submit a proposal **by Mar 5 (1 week before mid-term)**, and a final report **by May 14 (1 week after the final presentation)**

**Late Day Policy**

Students may request one 3-day extension in the semester for full credit. Otherwise, late submission within 3 days results in at most 80% of credits. Submission later than 3 days results in 0% of credits.

### Tentative Schedule

Note: This is an evolving list. For each topic, the presenter should cover 2-3 required papers in their presentation.

| **Date** | **Topic** | **Presenter** | **Reviewer** | **Note** |
| --- | --- | --- | --- | --- |
|  | **Course Introduction** |  |  |  |
| Jan 22 | Intro + Biology101 | Prof. Liu |  |  |
| Jan 27 | Diffusion |  |  |  |
| Jan 29 | Flow Models |  |  |  |
| Feb 3 | VAE  |  |  | Group Membership & Topic Preference Due |
| Feb 5 | Geometric DL & Equivariance |  |  |  |
| Feb 10 | Seq Model & Discrete Generation |  |  |  |
| Feb 12 | No Lecture / Brain storm for project proposal and prepare presentation |  |  |  |
|  | **Paper-reading lectures begin** |  |  |  |
|  | **Language Model in Biomedicine** |  |  |  |
| Feb 17 | lecture 1: protein | Kerui Chen, Wei Xia, Tao Feng | Jinwei Yao, Yexin Wu, Haofei Yu |  |
| Feb 19 | lecture 2: protein & beyond | Emmanuel Buabeng, Diya Yunus, Kriti Mathur | Xiao Lin, Zhichen Zeng, Zihao Li |  |
| Feb 24 | lecture 3: discrete generation | Enyi Jiang, Lily Xie, Huyen Nguyen | G2: Kerui Chen, Wei Xia, Tao Feng |  |
|  | **Molecule Generation** |  |  |  |
| Feb 26 | lecture 4: 2d | Xiao Lin, Zhichen Zeng, Zihao Li | G11: Reihaneh Jahedan, Akash Arunabharathi, Ishaan Mathur |  |
| Mar 3 | lecture 5: 3d | Reihaneh Jahedan, Akash Arunabharathi, Ishaan Mathur | G10: Reihaneh Jahedan, Akash Arunabharathi, Ishaan Mathur |  |
| Mar 5 | lecture 6: 2d & 3d | Jingjie He, Chenhao Xu, Boyang Sun | G6: Emmanuel Buabeng, Diya Yunus, Kriti Mathur | Proposal Due |
|  | **Mid-term Presentation & Hands on challenge introduction** |  |  |  |
| Mar 10 |  |  |  |  |
| Mar 12 |  |  |  |  |
|  | **Spring Break** |  |  |  |
| Mar 17 | No Lecture |  |  |  |
| Mar 19 | No Lecture |  |  |  |
|  | **Paper-reading Lectures** |  |  |  |
|  | **Protein Generation** |  |  |  |
| Mar 24 | lecture 7: folding and inverse folding | Jinwei Yao, Yexin Wu, Haofei Yu | G4: John Wu, Siddhartha Laghuverapu, Jathurshan Pradeepkumar |  |
| Mar 26 | lecture 8: folding and inverse folding | Hanyang Chen, Hangke Sui, Hesun Chen | G8: Ziwen Wang, Maohong Liao, Jiajun Fan |  |
| Mar 31 | lecture 9: folding and inverse folding |  |  |  |
| Apr 2 | lecture 10: co-design |  |  |  |
|  | **Complex-based Generation** |  |  |  |
| Apr 7 | lecture 11: peptide design |  |  |  |
| Apr 9 | lecture 12: structure-based drug design | John Wu, Siddhartha Laghuverapu, Jathurshan Pradeepkumar |  |  |
| Apr 14 | lecture 13: docking |  |  |  |
| Apr 16 | lecture 14: antibody design |  |  |  |
|  | **RLHF/DPO/Guidance** |  |  |  |
| Apr 21 | lecture 15 | Ziwen Wang, Maohong Liao, Jiajun Fan | G9: Eleanor Wedell, Yasamin Tabatabaee, James Willson |  |
| Apr 23 |  |  |  | Remote, DLL for challenge submission |
| Apr 28 | No Lecture / Work on Final Presentation |  |  |  |
| Apr 30 | No Lecture / Work on Final Presentation |  |  |  |
|  | **Final Presentation** |  |  |  |
| May 5 |  |  |  |  |
| May 7 |  |  |  |  |
| May 14 |  |  |  | Final Report due |

### Reading List

[Full Reading List](./ReadingList.md)

### Guidelines

**Presentation & Slides**

- 40-45 min presentation, at least 20 pages
- cover the content of required papers (paper above **optional**)
- be ready to answer questions
- you are encouraged to read some of those optional readings but not required

**Pre-class Questions**

- every group should submit at least 1 question or idea before class

**Review**

Review template (reference from ICLR 2025):

- Summary
[Provide a brief summary of the paper, including the main problem being addressed, key contributions, and proposed methods.]

- Evaluation Scores (1: poor, 2: weak, 3: fair, 4: good, 5: excellent)
Soundness: [Score: 1-5] (Does the paper provide a sound and well-supported argument?)
Presentation: [Score: 1-5] (Is the paper clearly written and well-structured?)
Contribution: [Score: 1-5] (Does the paper make a meaningful contribution to the field?)

- Strengths
[List the key strengths of the paper. Be specific about the aspects that are well-executed, such as novelty, clarity, experimental design, or real-world applicability.]

- Weaknesses
[Identify limitations or areas where the paper could be improved. Be constructive and suggest ways to address the issues.]

- Questions
[Pose specific questions for clarification and provide constructive suggestions for improvement.]

- Ethical Considerations
 Ethics review needed
 No ethics review needed
[Comment on potential ethical concerns, such as bias, data privacy, or misuse of the method.]

- Final Recommendation

    - Rating: [Score: 1-10] (How strong is this paper in its current form?)
    - Confidence Level: [Score: 1-5] (How confident are you in your assessment?)

| rating | meaning |
| --- | --- |
| 10 | Strong accept (Top 5% of ICLR submissions, a must-accept) |
| 9 | Clear accept (Excellent work, high confidence in acceptance) |
| 8 | Accept (Solid contribution, well-executed research) |
| 7 | Weak accept (Good paper but with some minor issues) |
| 6 | Marginally above the acceptance threshold (Could be accepted, but not strong) |
| 5 | Marginally below the acceptance threshold (Has merit but concerns remain) |
| 4 | Weak reject (Not strong enough for ICLR, requires major improvements) |
| 3 | Reject (Significant issues, not suitable for ICLR in its current form) |
| 2 | Strong reject (Serious flaws, major revisions needed before resubmission) |
| 1 | Trivial/invalid submission (Should not have been submitted in its current state) |

| confidence level | meaning |
| --- | --- |
| 5 | Very confident – The reviewer is an expert in the topic and fully understands the paper. It is highly unlikely that they missed something important. |
| 4 | Confident – The reviewer is familiar with the topic and reasonably certain about their assessment. There is a small chance they missed something. |
| 3 | Moderately confident – The reviewer understands the general ideas but is not deeply familiar with all technical details. Some aspects may require further verification. |
| 2 | Limited confidence – The reviewer is not very familiar with the topic and may have misunderstood some aspects. Additional expert opinions are needed. |
| 1 | Not confident – The reviewer does not feel qualified to assess the paper. They are unsure if their judgment is correct and strongly recommend additional expert input. |

**Rebuttal**

The rebuttal phase provides authors with an opportunity to clarify misunderstandings, address reviewer concerns, and strengthen their paper’s positioning. Below are key guidelines to ensure an effective response:

- Address Key Concerns First
Focus on the most critical points raised by the reviewers, such as concerns about methodology, experimental validity, and novelty.
Prioritize addressing low scores in soundness, contribution, or presentation, as these impact acceptance chances the most.

- Be Clear, Concise, and Professional
Stick to the facts: Provide clear, well-structured responses rather than lengthy justifications.
Maintain a professional tone: Avoid defensive language. Acknowledge valid points and explain improvements or clarifications.

- Provide Additional Evidence (If Possible)
If a reviewer questions experimental validity, clarify the setup and assumptions.
If applicable, include new results or brief additional analysis (e.g., ablation studies, comparisons with missing baselines).
If a misunderstanding occurred, restate your approach clearly and provide citations if necessary.

- Organize Responses for Readability
Summarize key points before responding to each review.
Use clear formatting, such as bullet points or bolded keywords, to make the response easy to follow.
Address each reviewer separately, referencing their comments explicitly (e.g., Reviewer 2 questioned the experimental setup...).

- Do Not Introduce Major Changes
The rebuttal is for clarifications and justifications, not for significant changes to the method or experiments.
If major revisions are needed, acknowledge them and indicate how they will be addressed in a future version.

**Experiment Report**

todo

**Final Report**

todo

### **Acknowledgements**

In course structure design, this course is heavily inspired by other seminar-like courses, particularly [UIUC CS598-GenAI System](https://github.com/fanlai0990/CS598). Acknowledgments to [Prof. Fan Lai](https://fanlai.me/) for  generous sharing of his great course.
