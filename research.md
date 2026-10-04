# Research Overview

## Table Reasoning: Knowing What Evidence Is Enough

### 1. Background and Motivation

Large language models (LLMs) are increasingly used to answer questions about tabular data. However, answering these questions correctly requires more than finding a relevant value in a table. A model must identify the information needed to answer the question, reason over the available evidence, and determine whether that evidence is sufficient to support an answer.

A key problem occurs when some information is missing. A model might still provide an answer even when the available evidence does not justify it, potentially leading to incorrect or unsupported conclusions. On the other hand, a model might reject a question as unanswerable even when the available information is sufficient.

This project investigates how reliably LLMs reason about evidence when answering questions over tables, particularly when some information is unavailable.

### 2. Research Questions

RQ1: Identifying Required Evidence

Can LLMs identify the evidence needed to answer a question about a table? Which types of questions are more difficult for them?

RQ2: Judging Evidence Sufficiency

Given a question and a complete or partially available table, can LLMs determine whether the available evidence is sufficient to answer the question?

RQ3: Identifying Supporting Evidence

Can LLMs identify the parts of a table that support their answers? How does table structure affect their ability to identify and use the relevant evidence?

### 3. Key Concepts

* **Evidence relevance:** Whether information in a table is related to the question.
* **Evidence sufficiency:** Whether the available information is enough to justify an answer.
* **Answer correctness:** Whether the answer matches the correct answer established for the question.
* **Supporting evidence:** The table cells, rows, columns, or other information that justify an answer.
* **Insufficient evidence:** A situation in which the available information does not uniquely justify an answer.

Missing information does not automatically mean that evidence is insufficient. If the missing information cannot change the answer, the available evidence may still be sufficient.

For example, if Mathematics has an enrollment increase of 40 students and Physics's increase is known to be at most 30, Mathematics can be identified as having the largest increase even if Physics's exact enrollment is missing.

### 4. Proposed Approach

We plan to investigate these questions using existing table question-answering and reasoning benchmarks.

The initial approach is to:

1. Review relevant literature and identify suitable benchmarks.
2. Select a benchmark and understand its tables, questions, answers, and annotations.
3. Establish a baseline using the original examples.
4. Create controlled variations of selected examples, such as removing cells or other relevant information.
5. Determine whether the evidence in each variation is sufficient to answer its question.
6. Evaluate selected LLMs using consistent prompts and evaluation criteria.
7. Analyze model performance and categorize common errors.

Possible experimental conditions include:

* Complete evidence.
* Missing information that could change the answer.
* Missing information that cannot change the answer because of other available constraints.
* Different table structures, where appropriate to the research questions.

These are proposed directions, not finalized experimental decisions.

### 5. Evaluation

We will consider evaluating the following abilities separately:

* **Answer accuracy:** Does the model provide the correct answer when the evidence is sufficient?
* **Sufficiency judgment:** Does the model correctly determine whether the evidence is sufficient?
* **Evidence identification:** Does the model identify the information needed to answer the question?
* **Evidence grounding:** Does the model cite table information that actually supports its answer?

We will also examine common failure cases, including unsupported guesses, incorrect sufficiency judgments, and the use of irrelevant or incomplete evidence.

The exact metrics, datasets, models, and evaluation procedures remain to be decided.

### 6. Related Work and Datasets

Potential starting points for the literature review include:

* **WikiTableQuestions:** A benchmark for answering questions over tables.
* **TabFact:** A benchmark for verifying statements using table evidence.

These are candidate resources rather than confirmed dataset choices. We will review their suitability, annotations, licensing, and relevance to our research questions before selecting a benchmark.

Relevant papers, their main contributions, limitations, and connections to this project will be documented as the literature review progresses.

### 7. Expected Contribution

The goal is to better understand whether LLMs can distinguish between having enough evidence to answer a question and merely having enough information to produce a plausible answer.

The project will investigate how missing information affects model behavior and whether models can recognize when they should answer, when they should identify limitations in the available evidence, and which table information supports their conclusions.

The specific contribution will be refined after reviewing related work and finalizing the experimental design.

### 8. Current Status and Open Decisions

**Current stage:** Research planning and initial exploration.

Decisions still to be made:

* Which research question will be the primary focus?
* Which benchmark or benchmarks should be used?
* How will evidence sufficiency be defined and annotated?
* Which models will be evaluated?
* Which types of missing information and table modifications will be tested?
* Which metrics will be used?
* How will the experiment be kept reproducible?

These decisions will be refined through literature review, discussions with the prof, and initial experiments.
