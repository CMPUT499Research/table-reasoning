# Table Evidence Identification Task

You will receive a single document containing **30 questions**, each accompanied by its corresponding table.

Your task is to answer each question using only its provided table and identify the evidence cells needed to support the answer.

These instructions apply to all 30 questions.

---

## 1. Input Format

The document contains 30 sections formatted as follows:

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
- **Table:** The table contents, including row and column coordinates.
- **Question:** The question to answer using the table.

Row and column indices start at `0`. Header rows are included in the numbering.

---

## 2. Instructions

For each of the 30 questions:

1. Read the question and its associated table carefully.
2. Use only the information provided in that question's table. Do not use external knowledge, internet searches, tools, or information from other questions.
3. Determine the answer based on the table contents.
4. Identify the specific table cells containing the evidence needed to derive the answer.
5. Provide a brief explanation of why those cells contain sufficient evidence to answer the question.
6. Return the result using the required structure below.

Treat each question independently. Do not combine evidence from different tables.

---

## 3. Required Output Format

Return a single Markdown table containing exactly **30 rows**, one for each question, in the same order as the input document.

Use these four columns:

| question_id | answer | evidence_cells | rationale |
|-------------|--------|----------------|-----------|
| ... | ... | ... | ... |

### Column Definitions

#### `question_id`

- Copy the exact `question_id` from the input document.
- Do not modify or generate new IDs.

#### `answer`

- Provide the answer derived from the corresponding table.
- Preserve the numerical value and units where applicable.
- Do not include explanations in this column.

#### `evidence_cells`

- Identify the table cells required to support the answer.
- Use coordinates in the format `(row, column)`.
- For multiple cells, use `[(row, column), (row, column)]`.
- Use the row and column numbering provided in the input document.
- Include only the cells needed to support the answer.

#### `rationale`

- Briefly explain how the identified evidence supports the answer.
- For direct lookups, explain which row and column identify the requested value.
- For calculations, explain the operation performed using the identified values.
- Keep the explanation concise and specific to the question.

---

## 4. Important Rules

- Answer all 30 questions.
- Use only the provided tables.
- Do not rely on outside information or assumptions.
- Do not use answers or evidence from one question to answer another.
- Do not invent values or cell coordinates.
- Do not include unnecessary evidence cells.
- If the table does not contain enough information to answer a question, write `INSUFFICIENT_EVIDENCE` in the answer column and briefly explain why in the rationale.
- Do not change the requested output structure.

---

## 5. Final Output

Return only the completed Markdown table with the following columns, in this exact order:

```text
question_id | answer | evidence_cells | rationale
```

Do not include an introduction, conclusion, summary, or any additional commentary.

**Process all 30 questions before returning the completed table.**
