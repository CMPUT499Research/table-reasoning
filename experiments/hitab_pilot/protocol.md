# HiTab RQ1 Pilot Protocol

## 1. Research question

Our first research question is:

**Can language models identify the evidence needed to answer a question about a table?**

For this pilot, each model receives a complete HiTab table and a question about that table. We want to see whether the model can identify the relevant cells and explain how they help answer the question.

This pilot focuses on evidence identification, not just whether the model gets the final answer right. We are not removing cells or testing what happens when information is missing yet. Those experiments may come later.

## 2. Dataset and sample

We use the [HiTab dataset](https://github.com/microsoft/HiTab), which contains questions about tables with hierarchical row and column structures.

- **Dataset split:** Development (`dev`)
- **Input file:** `data/dev_samples.jsonl`
- **Sample size:** 30 questions
- **Sampling seed:** `499`
- **Question registry:** `experiments/hitab_pilot/questions.csv`

The questions were selected by reading the non-empty JSONL records, sorting them by their string IDs, and randomly sampling 30 records with seed `499`. This procedure is implemented in `sample_questions.py`.

The sample is intended for developing and checking our experimental pipeline. We will keep the test split separate for a later evaluation.

The registry records the question, table ID, dataset information, and other details needed to prepare each model request. It does not include the gold answer or the annotations used to construct the human reference.

**Dataset version:** The protocol currently records commit `d179602662b490249baf068a76fbe4137029126e`. Before the experiment is finalized, we need to verify that this commit contains the exact development file used to generate our sample.

The dataset's license and terms of use should be reviewed before redistributing any dataset-derived material.

## 3. Preparing the tables

HiTab represents tables using both a hierarchical structure and a grid of cell text. We need to turn these representations into a format that models can understand without losing the relationships between row headers, column headers, and data cells.

For each question, the model will receive:
- The question text.
- The table's contents.
- The relevant row and column header paths for the data cells.

Each data cell will have a stable, zero-based coordinate. Header paths will show how a cell fits into the table's hierarchy, including nested headers and merged cells.

The planned serialization format is called `hitab-paths-v1`. We will finalize and test its implementation before using it for the experiment. Until then, it should be treated as a planned format rather than a completed component.

The model must not receive HiTab's gold answer, linked-cell annotations, answer formulas, or reference-cell mappings. These are reserved for preparing and evaluating the human reference.

## 4. Models

We plan to evaluate two hosted models in this pilot:

| Model | Access method | Role in the pilot |
|---|---|---|
| GLM-5.3 | NVIDIA API Catalog endpoint | Hosted model condition |
| Gemini | Google's Gemini API | Hosted model condition |

GLM-5.3 will be accessed through NVIDIA's API endpoint. Gemini will be accessed through Google's API.

Before running the full sample, we will confirm the exact model identifiers and available settings for both services. We will record the model version, endpoint or provider, decoding settings, output limits, and any other relevant configuration.

We will use the same table serialization, question, and evidence-identification instructions for both models. Where the APIs support comparable settings, we will keep those settings consistent. Any differences that cannot be aligned will be documented.

Both models are hosted services, so this pilot compares two API-accessed models rather than comparing a locally run open-weight model against a hosted model.

We will also record failed requests, malformed responses, retries, and other issues that could affect the results. We will not silently discard unsuccessful runs.

## 5. Prompt and output format

Both models will receive the same version of the evidence-identification prompt, identified as `hitab-rq1-v1`.

The prompt will ask each model to identify the evidence needed to answer the question and return its response in a structured format.

Before running the experiment, we will finalize the prompt and expected output schema. We will save the prompt version and its SHA-256 hash so that we can identify exactly which instructions were used.

If we change the prompt after testing begins, we will record the change and distinguish the affected runs rather than automatically combining them with earlier results.

## 6. Human reference and evaluation

We need a human reference for each question so that we can judge whether a model identified sufficient evidence.

Before reviewing model responses, we will prepare a reference packet for every sampled question. We will use the complete table and HiTab's existing answer and evidence annotations as starting points, then check the evidence ourselves.

Each reference packet will record:

- The data cells needed to support the answer.
- The relevant row and column header paths.
- The operation or comparison required to answer the question.
- Other acceptable evidence that could also justify the answer.

Where possible, two annotators will prepare or independently check the reference material. Differences will be discussed and resolved before evaluation. If only one annotator is available, we will record that the reference was prepared by a single annotator and report this as a limitation.

Evaluators will assess model responses without seeing which model produced them. They will judge the identified row paths, column paths, cells, and operations as `correct`, `partial`, or `incorrect`, then assign an overall evidence label.

Final-answer correctness will be recorded separately from evidence quality. A model may give the correct answer without identifying adequate supporting evidence, or identify useful evidence but make a mistake in its final answer.

We will accept alternative evidence sets when they are sufficient to justify the answer, even if they do not exactly match the preferred cells in the reference packet.

## 7. Files and records

The pilot files will be kept under `experiments/hitab_pilot/`.

- `questions.csv`: The selected questions and their metadata.
- `prompt.md`: The evidence-identification prompt.
- `protocol.md`: This experimental protocol.
- `results.csv`: Raw model responses and run configurations.
- `evaluations.csv`: Human evaluation labels.
- `reference_packets/`: The human-prepared evidence references.

We will keep raw model responses separate from human evaluation labels. API credentials will be stored outside the repository, and we will not commit credentials, model weights, or the raw HiTab dataset.

## 8. Limitations

This is a small pilot with 30 questions. Its main purpose is to check whether our data preparation, prompting, and evaluation procedures work as intended. It is not large enough to support broad claims about model performance or reliable rankings between models.

The dataset is publicly available, so we cannot rule out the possibility that some questions or tables appeared in model training data.

HiTab's existing annotations are useful for preparing the human references, but they may not capture every valid way to support an answer. Human checks and adjudication are therefore important.

Finally, the way we serialize the table may affect the results. We will test the serialization on a small number of examples before running the full pilot and document the final format used.