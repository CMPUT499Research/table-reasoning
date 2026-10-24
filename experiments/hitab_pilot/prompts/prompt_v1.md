# Table Evidence Identification — Version 1

## Required Output Format

For each question, return exactly one row in a Markdown table using the following columns in the specified order:

| **question_id** | **expected_answer** | **primary_question_type** | **evidence_cells** | **evidence_complexity** | **rationale(why evidence is enough?)** |
| --------------- | ------------------- | ------------------------- | ------------------ | ----------------------- | -------------------------------------- |

### Column Requirements

1. **question_id**: The exact question ID provided in the input. Do not modify it.

2. **expected_answer**: The answer to the question, based only on the provided table. Do not use external knowledge or make unsupported assumptions.

3. **primary_question_type**: Assign exactly one of the following categories:
   - `lookup`: Retrieving a value or piece of information directly from the table.
   - `arithmetic_aggregation`: Applying arithmetic or an aggregation operation, such as summing, averaging, or calculating a difference.
   - `comparison_ranking`: Comparing values or ranking items to identify the highest, lowest, or relative ordering.

4. **evidence_cells**: Identify the specific table cells needed to answer the question. Use the cell identifiers or coordinates provided in the input, if available. Otherwise, identify cells using their row labels, column headers, and values. Include all necessary evidence cells, but do not include irrelevant cells. If the answer cannot be determined from the provided table, state `INSUFFICIENT_EVIDENCE` and explain what is missing in the rationale.

5. **evidence_complexity**: Classify the evidence needed to answer the question as one of the following:
   - `low`: One cell or a small amount of directly accessible evidence is sufficient.
   - `medium`: Multiple cells must be combined, or the evidence requires a straightforward calculation or comparison.
   - `high`: Evidence requires combining information across multiple parts of the table, interpreting complex table structure, or performing more involved reasoning.

6. **rationale(why evidence is enough?)**: Briefly explain why the identified evidence cells are sufficient to answer the question. Describe the relationship between the evidence and the answer, including any required calculation or comparison. If the evidence is insufficient, explain precisely what information is missing and why the answer cannot be established.

### Output Rules

- Return only the Markdown table. Do not include introductory text, conclusions, code fences, or additional commentary.
- Use exactly the six column names specified above, in the specified order.
- Return one row for every input question, preserving the original `question_id`.
- Do not omit questions, combine multiple questions into one row, or add extra columns.
- Do not invent cell identifiers, cell values, or evidence that are not present in the input.
- Distinguish between evidence that supports an answer and evidence that merely provides context.
- Identify the minimum sufficient evidence needed to answer the question.
- If multiple cells are jointly necessary, identify each of them.
- If the answer cannot be determined from the table, do not guess. Use `INSUFFICIENT_EVIDENCE` for `expected_answer` and `evidence_cells`, and explain the limitation in the rationale.
- Ensure that Markdown table cells do not contain unescaped pipe characters (`|`).
- Use concise, specific rationales rather than generic statements such as "the evidence supports the answer."
