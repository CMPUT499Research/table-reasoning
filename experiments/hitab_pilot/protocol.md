# HiTab Evidence Identification Protocol

## 1. Research Question

This experiment primarily addresses **RQ1**:

> **Can language models identify the evidence needed to answer a question, and for what types of questions is this difficult?**

The goal is not only to determine whether a model produces the correct answer. We also evaluate whether the model identifies table cells that are sufficient to derive and justify that answer.

This distinction is important because a model may produce a correct answer while citing incomplete, incorrect, or irrelevant evidence.

The broader project also investigates:

- **RQ2 — Evidence sufficiency:** Given a question and only part of a table, can a model determine whether the available evidence is sufficient to answer it?
- **RQ3 — Evidence support and structure:** Can a model accurately identify which parts of a table support its answer, and how do properties of the table's structure affect its reasoning?

The experiments in this directory currently focus primarily on **RQ1**. Controlled evidence-removal experiments for RQ2 are planned separately.

---

## 2. Experimental Stages

The work in this directory contains two related but distinct stages.

### Stage 1 — 30-question mixed pilot

The original pilot contains **30 questions sampled from the HiTab development split**.

The sample contains questions requiring different forms of reasoning:

- `lookup`
- `arithmetic_aggregation`
- `comparison_ranking`

This stage is used to evaluate whether models can identify supporting evidence across multiple types of table questions.

The fixed question registry is stored in:

- [`questions.csv`](questions.csv)

The sampling procedure is stored in:

- [`sample_questions.py`](sample_questions.py)

### Stage 2 — Comparison/ranking-focused experiment

A later experiment focuses specifically on **comparison and ranking questions**.

This experiment uses **50 questions** and a more explicit definition of sufficient evidence. In particular, models are instructed that identifying only the winning or selected value is not necessarily enough to establish a comparison or ranking.

The prompt for this condition is:

- [`prompts/prompt_v3.md`](prompts/prompt_v3.md)

This 50-question experiment is a separate experimental condition and should not be merged with the original 30-question mixed pilot when reporting results.

Its question registry, model outputs, and evaluation results should be stored separately once finalized.

---

## 3. Dataset and Sampling

The experiments use the [HiTab](https://github.com/microsoft/HiTab) dataset.

HiTab contains question-answer pairs associated with tables that may contain hierarchical row and column structures.

For the 30-question pilot:

| Item | Value |
| --- | --- |
| Dataset split | Development (`dev`) |
| Source file | `data/dev_samples.jsonl` |
| Sample size | 30 questions |
| Sampling seed | `499` |
| Dataset revision recorded in registry | `d179602662b490249baf068a76fbe4137029126e` |

The sampling script:

1. reads all non-empty examples from the HiTab development JSONL file;
2. sorts examples by question ID;
3. initializes Python's random sampler with seed `499`;
4. randomly selects 30 questions; and
5. writes the selected questions and their metadata to `questions.csv`.

The resulting 30-question sample is treated as fixed and is not resampled between model runs.

The HiTab test split is not used for this pilot.

---

## 4. Table Representation

Each question is paired with its corresponding complete HiTab table.

For the current experiments, tables are presented to models in a text representation with explicit row and column coordinates.

A typical table is represented as:

```text
Table title: ...

Row 0: [0] ... | [1] ... | [2] ...
Row 1: [0] ... | [1] ... | [2] ...
...
```

Row and column indices begin at `0`.

Header rows are included in the row numbering.

Each model receives:

- the `question_id`;
- the `table_id`;
- the table title;
- the complete table contents with coordinates; and
- the question.

The model is instructed to reason only from the supplied table.

The model does **not** receive the human gold annotations when generating its response.

The current `questions.csv` records `table_serialization_version` as `not_implemented`. Therefore, this protocol does not refer to the representation as `hitab-paths-v1` or claim that a finalized serialization format exists.

If a formal serialization format is introduced later, it should receive a version identifier and be documented separately.

---

## 5. Human Gold Annotations

Two annotators independently reviewed the original 30 questions:

- Ahmed
- Shula

Their annotations are stored in:

- [`30QA_gold_annotation_ajax.csv`](30QA_gold_annotation_ajax.csv)
- [`30QA_gold_annotation_shula.csv`](30QA_gold_annotation_shula.csv)

For each question, the annotation records:

| Field | Description |
| --- | --- |
| `question_id` | HiTab question identifier |
| `expected_answer` | Human-determined answer |
| `primary_question_type` | Main reasoning type |
| `evidence_cells` | Cells needed to derive and justify the answer |
| `evidence_complexity` | Description of how much evidence is required |
| `rationale(why evidence is enough?)` | Explanation of why the selected evidence is sufficient |

The three primary question types are:

- `lookup`
- `arithmetic_aggregation`
- `comparison_ranking`

The two annotation files are **independent annotations**, not two separate gold standards.

Disagreements should be reviewed and adjudicated before final results are reported. The adjudicated version should become the final human reference.

Minor label inconsistencies such as `single_cell`, `single_cells`, `multiple_cell`, and `multiple_cells` should also be normalized during adjudication rather than silently interpreted during analysis.

---

## 6. Definition of Sufficient Evidence

The central concept in this experiment is **evidence sufficiency**.

Evidence is considered sufficient when the cited cells, together with the question, allow a reader to reproduce the reasoning and verify why the answer is correct.

The goal is therefore not simply to locate a cell containing the final answer.

### Lookup questions

For a direct lookup, a single value cell may be sufficient when the question and table structure uniquely determine what that cell represents.

Identifying row or column labels may also be necessary when the value cannot be interpreted unambiguously without them.

### Arithmetic and aggregation questions

The evidence must include the values needed to perform the required operation.

For example, if the answer requires:

```text
48.4 - 32.8 = 15.6
```

both source values are necessary evidence.

Providing only `15.6` or only one of the two source values is not sufficient evidence for the calculation.

### Comparison and ranking questions

Evidence must establish the comparison being claimed.

For example, if a question asks which of two groups has the higher value, citing only the selected group's value is insufficient. The evidence must also contain the value needed for the relevant comparison.

Likewise, for a maximum or minimum question, the cited evidence must be sufficient to establish that the selected candidate satisfies the requested ranking.

This distinction is especially important in the comparison/ranking-focused experiment.

---

## 7. Prompt Versions

Prompt development occurred iteratively. All prompt versions are retained because changes in instructions may affect model behaviour.

### Prompt V1

File:

- [`prompts/prompt_v1.md`](prompts/prompt_v1.md)

V1 is the original evidence-identification prompt.

It asks the model to return:

1. `question_id`
2. `expected_answer`
3. `primary_question_type`
4. `evidence_cells`
5. `evidence_complexity`
6. `rationale(why evidence is enough?)`

This version asks the model not only to identify evidence but also to classify the question type and evidence complexity.

### Prompt V2

File:

- [`prompts/prompt_v2.md`](prompts/prompt_v2.md)

V2 simplifies the output to:

1. `question_id`
2. `answer`
3. `evidence_cells`
4. `rationale`

It is designed for the complete 30-question document and focuses more directly on answer correctness and evidence identification.

### Prompt V3

File:

- [`prompts/prompt_v3.md`](prompts/prompt_v3.md)

V3 is designed specifically for a **50-question comparison/ranking experiment**.

It strengthens the definition of sufficient evidence by explicitly requiring models to include the values needed to establish a comparison or ranking.

For example, models are instructed not to cite only the selected answer cell when additional cells are required to demonstrate that the answer is the highest, lowest, greater, smaller, more likely, or less likely alternative.

### Prompt-version separation

Results produced using different prompt versions should not automatically be treated as belonging to the same experimental condition.

The prompt version used for a run should be recorded with the corresponding model output.

If results from multiple prompt versions are compared, the prompt difference must be treated as an experimental difference rather than ignored.

---

## 8. Models

The current repository contains graded pilot responses for three model conditions:

- **DeepSeek**
- **Gemini Flash**
- **GPT-6**

The corresponding files are:

- [`model_responses/deepseek_pilot_graded.csv`](model_responses/deepseek_pilot_graded.csv)
- [`model_responses/gemini_flash_pilot_graded.csv`](model_responses/gemini_flash_pilot_graded.csv)
- [`model_responses/gpt_6_pilot_graded.csv`](model_responses/gpt_6_pilot_graded.csv)

The earlier plan to use GLM 5.3 is no longer part of the current protocol.

For final reporting, each run should record, where available:

- exact model name and version;
- provider;
- prompt version;
- date of execution;
- generation settings; and
- any relevant API or runtime configuration.

These details should not be reconstructed from memory after the experiment.

---

## 9. Model Procedure

Within a given experimental condition, each model receives the same question-table input and the same prompt instructions.

For the 30-question condition, the complete document contains all 30 questions and their corresponding tables.

For each question, the model must:

1. read the question;
2. reason only from the supplied table;
3. determine an answer;
4. identify the supporting evidence cells; and
5. explain why those cells are sufficient.

Models are explicitly instructed not to:

- use external knowledge;
- search the internet;
- combine information across questions;
- invent values;
- invent coordinates; or
- guess when the table does not provide sufficient evidence.

When the provided table is insufficient, the prompt instructs the model to return `INSUFFICIENT_EVIDENCE`.

---

## 10. Evaluation

Answer quality and evidence quality are evaluated separately.

The current graded response files contain two primary evaluation fields:

- `answer_correctness`
- `evidence_correctness`

Both are treated as binary indicators:

```text
1 = correct
0 = incorrect
```

### Answer correctness

`answer_correctness = 1` when the model's final answer agrees with the adjudicated human answer, allowing equivalent formatting where appropriate.

Examples of formatting differences that should not by themselves cause failure include:

- `30` versus `30%`, when the table clearly uses percentage units;
- capitalization differences;
- comma formatting in large numbers; and
- equivalent numerical precision where the intended answer is unchanged.

### Evidence correctness

`evidence_correctness = 1` when the cited evidence is sufficient to derive and justify the model's answer.

Evidence should be marked incorrect when, for example:

- the model cites the wrong cells;
- required source values are missing;
- a comparison cites only one side of the comparison;
- a ranking cites only the selected value without enough evidence to establish the ranking;
- the model invents a coordinate;
- the cited cells do not support the stated calculation; or
- the evidence is unrelated to the answer.

Exact coordinate agreement with one annotator is not required if the model identifies a different evidence set that is genuinely sufficient.

Evidence grading should therefore evaluate **sufficiency**, not merely exact string matching against a gold annotation.

---

## 11. Primary Metrics

Answer and evidence performance are reported separately.

### Answer accuracy

```text
Answer Accuracy =
number of questions with correct answers
----------------------------------------
total number of evaluated questions
```

### Evidence accuracy

```text
Evidence Accuracy =
number of questions with sufficient evidence
--------------------------------------------
total number of evaluated questions
```

Because answer correctness and evidence correctness are separate, four outcomes are possible:

| Answer | Evidence | Interpretation |
| --- | --- | --- |
| Correct | Correct | Model answered correctly and justified it correctly |
| Correct | Incorrect | Model reached the right answer without sufficient evidence |
| Incorrect | Correct | Model identified useful evidence but failed in reasoning or final answer |
| Incorrect | Incorrect | Both answer and evidence failed |

Results should also be examined by question type:

- lookup;
- arithmetic/aggregation; and
- comparison/ranking.

The comparison/ranking follow-up should be analyzed separately because it uses a different question distribution and a more specific prompt.

---

## 12. Failure Analysis

In addition to aggregate accuracy, model errors should be examined qualitatively.

Useful failure categories include:

- wrong cell;
- missing evidence cell;
- incomplete comparison;
- incomplete ranking;
- wrong arithmetic operation;
- correct evidence but incorrect reasoning;
- correct answer with insufficient evidence;
- unnecessary or over-inclusive evidence;
- row/column misinterpretation;
- header or table-structure confusion; and
- unsupported answer.

These categories are intended to help explain **how evidence reasoning fails**, rather than only measuring whether it fails.

---

## 13. Files

The current pilot directory contains:

```text
experiments/hitab_pilot/
├── README.md
├── protocol.md
├── questions.csv
├── sample_questions.py
├── 30QA_gold_annotation_ajax.csv
├── 30QA_gold_annotation_shula.csv
│
├── prompts/
│   ├── prompt_v1.md
│   ├── prompt_v2.md
│   └── prompt_v3.md
│
└── model_responses/
    ├── deepseek_pilot_graded.csv
    ├── gemini_flash_pilot_graded.csv
    └── gpt_6_pilot_graded.csv
```

### File purposes

| File | Purpose |
| --- | --- |
| `questions.csv` | Fixed 30-question HiTab sample |
| `sample_questions.py` | Reproducible sampling script |
| `30QA_gold_annotation_ajax.csv` | Ahmed's independent human annotation |
| `30QA_gold_annotation_shula.csv` | Shula's independent human annotation |
| `prompts/prompt_v1.md` | Initial evidence-identification prompt |
| `prompts/prompt_v2.md` | Revised 30-question prompt |
| `prompts/prompt_v3.md` | Comparison/ranking-focused 50-question prompt |
| `model_responses/*.csv` | Model responses with manual grading |

The two human annotation files should eventually be followed by a final adjudicated gold annotation file.

---

## 14. Limitations

The original pilot contains only 30 questions. It is useful for developing and testing the evidence-identification methodology, but it is too small to support broad claims about language-model performance.

HiTab is publicly available, so some questions or tables may have appeared in model training data.

Human evidence annotation also involves judgment. Multiple evidence sets may legitimately support the same answer, especially in complex tables. This is why model evidence should be evaluated for sufficiency rather than only exact agreement with one reference set.

Prompt wording can substantially affect evidence behaviour. Results obtained using V1, V2, and V3 should therefore not be pooled without accounting for the prompt condition.

The table representation may also influence performance. The current experiments use explicit row and column coordinates, and results should be interpreted as model performance under that representation.

Finally, the current human annotations have not yet been replaced by a single adjudicated gold file. Final reported results should use the adjudicated reference rather than arbitrarily choosing one annotator's version.

---

## 15. Intended Contribution

The purpose of this work is not simply to create another table question-answering accuracy benchmark.

The broader goal is to develop a framework for evaluating whether language models understand **what evidence is needed to support an answer**.

The planned progression is:

> **correct answer → correct evidence → sufficient evidence → knowing when evidence is missing**

The project aims to contribute:

1. an evidence-identification evaluation protocol for table question answering;
2. human gold annotations describing sufficient evidence;
3. analysis of evidence-identification failures across reasoning types;
4. targeted comparison/ranking experiments where sufficiency is especially important; and
5. controlled evidence-removal experiments for testing whether models recognize insufficient evidence.
