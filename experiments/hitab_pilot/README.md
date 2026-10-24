# HiTab pilot: identifying evidence in tables

This directory contains the pilot study for our first research question:

> Can a language model identify the evidence needed to answer a question?

The study tests whether models can find enough evidence in a table to support an answer. Answer accuracy alone is not enough: a model may reach the right answer while citing incomplete or irrelevant evidence.

## 1. Dataset

We use [HiTab](https://github.com/microsoft/HiTab), a question-answering dataset built from tables with hierarchical row and column headers.

For this pilot, we used seed `499` to randomly sample 30 questions from the development split. The sample covers three types of questions:

- Lookup questions, which ask for information stated directly in a table
- Arithmetic and aggregation questions, which require calculations based on table values
- Comparison and ranking questions, which require values to be compared or ordered

The sampled questions and the script used to select them are available in [questions.csv](questions.csv) and [sample_questions.py](sample_questions.py).

## 2. Human annotations

Two annotators reviewed the 30 questions independently. For each question, they recorded the expected answer, question type, relevant cells, evidence complexity, and a short explanation of why the selected evidence was sufficient.

| Annotator | File |
| --- | --- |
| Ahmed | [30QA_gold_annotation_ajax.csv](30QA_gold_annotation_ajax.csv) |
| Shula | [30QA_gold_annotation_shula.csv](30QA_gold_annotation_shula.csv) |

These annotations serve as the human reference for evaluating model responses. Any disagreements between the two sets of annotations must be reviewed before we create the final adjudicated gold standard.

## 3. Prompts

We tested several versions of the prompt as we refined how models should identify and report evidence. All versions are included so that the experiment can be reproduced and the changes between runs can be tracked.

| Version | Description | File |
| --- | --- | --- |
| V1 | The original prompt, which asks for the question type, evidence cells, and evidence complexity | [prompt_v1.md](prompts/prompt_v1.md) |
| V2 | A revised prompt used to answer the 30 questions and identify supporting cells | [prompt_v2.md](prompts/prompt_v2.md) |
| V3 | A prompt for comparison and ranking questions, with more emphasis on evidence that fully supports a comparison | [prompt_v3.md](prompts/prompt_v3.md) |

Each prompt asks the model to return a structured Markdown table, which makes the responses easier to review and compare.

## 4. Model responses

The pilot includes graded responses from three language models(prompt_v2 was used):

| Model | Results |
| --- | --- |
| DeepSeek | [deepseek_pilot_graded.csv](model_responses/deepseek_pilot_graded.csv) |
| Gemini Flash | [gemini_flash_pilot_graded.csv](model_responses/gemini_flash_pilot_graded.csv) |
| GPT-6 | [gpt_6_pilot_graded.csv](model_responses/gpt_6_pilot_graded.csv) |

We grade both the final answer and the evidence cited in support of it.

## 5. Evaluation

The evaluation asks five questions about each response:

1. Is the final answer correct?
2. Did the model identify the relevant table cells?
3. Are those cells sufficient to derive and justify the answer?
4. Did the model include cells that are unrelated or redundant?
5. Do certain question types lead to recurring errors?

This distinction matters because a correct answer does not guarantee that the model found the right evidence. For example, a model might select the largest value in a table but cite only that value. Without the other values being compared, the cited evidence does not establish that it is the largest.

## 6. Workflow

The pilot uses the following process:

1. Sample questions from HiTab.
2. Retrieve the tables associated with those questions.
3. Annotate the evidence independently.
4. Give each model the questions and corresponding tables.
5. Collect the model responses in a consistent format.
6. Compare the cited evidence with the human annotations.
7. Review answer accuracy, evidence sufficiency, and common errors.

The original study design is documented in [protocol.md](protocol.md). Some prompt formats and model choices have changed since that protocol was written.

## Project information

- **Title:** Table Reasoning: Knowing What Evidence Is Enough
- **Course:** CMPUT 499, University of Alberta
- **Researchers:** Ahmed Jama and Shula
- **Repository:** [CMPUT499Research/table-reasoning](https://github.com/CMPUT499Research/table-reasoning)
