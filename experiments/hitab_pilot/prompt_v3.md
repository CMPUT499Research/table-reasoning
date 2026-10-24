# Table Evidence Identification Task

You will receive a single document containing **50 questions**, each accompanied by its corresponding table.

All questions require some form of **comparison or ranking reasoning**.

Your task is to answer each question using only its provided table and identify the **sufficient evidence cells needed to derive and justify the answer**.

These instructions apply to all 50 questions.

---

## 1. Input Format

The document contains 50 sections formatted as follows:

```text
=== QUESTION 1 ===

question_id: ...

table_id: ...

Table title: ...

Table (cells are written as [column] value; row and column numbers start at 0 and count header rows):

Row 0: [0] ... | [1] ... | [2] ...
Row 1: [0] ... | [1] ... | [2] ...
...

Question: ...
```

Each section contains:

- **question_id:** A unique identifier for the question.
- **table_id:** The identifier of the associated table.
- **Table title:** The title describing the table.
- **Table:** The complete table contents, including row and column coordinates.
- **Question:** The question to answer using the table.

Row and column indices start at `0`. Header rows are included in the numbering.

---

## 2. Task

For each of the 50 questions:

1. Read the question and its associated table carefully.
2. Use only the information provided in that question's table.
3. Determine the answer based on the table contents.
4. Identify the table cells that are **necessary and sufficient to derive and justify the answer**.
5. Provide a brief explanation of how those cells establish the answer.
6. Return the result using the required structure below.

Treat each question independently. Do not combine evidence from different tables.

---

## 3. Evidence Sufficiency

The goal is not merely to identify a cell containing the final answer.

The evidence cells should contain enough information for another reader to **derive and verify why the answer is correct from the table**.

For comparison and ranking questions:

- Include the values necessary to establish the required comparison or ranking.
- If the question asks which of two items is greater, lower, more likely, less likely, etc., include the cells needed to compare those items.
- If the question asks for a maximum, minimum, highest, lowest, most, least, or other ranking across several candidates, include the cells needed to establish that the selected answer satisfies that condition.
- Do not cite only the selected answer's cell if that cell alone does not demonstrate the required comparison.
- Include identifying cells, such as row or column labels, when they are necessary to determine which entity a numerical value belongs to.
- Do not include unrelated cells that are not needed to establish the answer.

Evidence is **sufficient** when a reader could use the cited cells and the question to reproduce the reasoning and verify the answer without relying on unstated information from the rest of the table.

---

## 4. Required Output Format

Return a single Markdown table containing exactly **50 rows**, one for each question, in the same order as the input document.

Use these four columns:

```markdown
| question_id | answer | evidence_cells | rationale |
|-------------|--------|----------------|-----------|
| ... | ... | ... | ... |
```

### `question_id`

- Copy the exact `question_id` from the input document.
- Do not modify or generate new IDs.

### `answer`

- Provide the answer derived from the corresponding table.
- Preserve numerical values and units where applicable.
- Do not include explanations in this column.

### `evidence_cells`

- Identify all table cells necessary and sufficient to derive and justify the answer.
- Use coordinates in the format:

```text
(row, column)
```

- For multiple cells, use:

```text
[(row, column), (row, column)]
```

- Use the row and column numbering provided in the input document.
- Do not invent cell coordinates.
- Do not include cells merely because they are nearby.
- Do not omit a required comparison cell simply because the final answer has already been identified.

### `rationale`

- Briefly explain how the cited evidence establishes the answer.
- Explicitly describe the comparison or ranking performed.
- Mention the relevant values when useful.
- Keep the explanation concise and specific to the question.

For example, the rationale should make clear why the selected value is higher, lower, greatest, smallest, more likely, less likely, etc., than the relevant alternative values.

---

## 5. Important Rules

- Answer all 50 questions.
- Use only the provided table for each question.
- Do not use external knowledge, internet searches, tools, or information from other questions.
- Do not use answers or evidence from one question to answer another.
- Do not invent values or coordinates.
- Do not include unnecessary evidence cells.
- Evidence must be sufficient to **justify the comparison or ranking**, not merely locate the final answer.
- If the table does not contain enough information to establish the requested comparison or ranking, write `INSUFFICIENT_EVIDENCE` in the `answer` column.
- If evidence is insufficient, include the available relevant cells where appropriate and briefly explain what required comparison information is missing.
- Do not change the requested output structure.

---

## 6. Final Output

Return **only** the completed Markdown table with the following columns, in this exact order:

```text
question_id | answer | evidence_cells | rationale
```

Do not include an introduction, conclusion, summary, notes, or additional commentary.

**Process all 50 questions before returning the completed table.**
