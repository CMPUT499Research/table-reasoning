"""
Build the reproducible 50-question HiTab comparison/ranking evaluation set.

The script:

1. Reads questions from HiTab's quality-checked test split.
2. Identifies comparison/ranking questions using HiTab aggregation operators
   plus manually audited inclusions and exclusions.
3. Sorts the candidate pool by question ID.
4. Randomly samples 50 questions using seed 499.
5. Loads the corresponding complete tables from tables.zip.
6. Writes a model-ready text file containing the 50 questions and tables.
7. Writes metadata describing the selected sample.
8. Records provenance information needed to reproduce the sample.

No language model or external API is used by this script.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import random
import re
import zipfile
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SEED = 499
SAMPLE_SIZE = 50

DATASET_REVISION = "d179602662b490249baf068a76fbe4137029126e"

DATASET_RELATIVE_PATH = "data/test_samples_qualitycheck.jsonl"
TABLE_ARCHIVE_RELATIVE_PATH = "data/tables.zip"

CLASSIFICATION = "comparison_ranking"

# This script is expected to live at:
#
# experiments/hitab_pilot/sample_comparison_50.py
#
# parents[2] therefore refers to the repository root.
REPO_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = REPO_ROOT / DATASET_RELATIVE_PATH
TABLE_ARCHIVE_PATH = REPO_ROOT / TABLE_ARCHIVE_RELATIVE_PATH

OUTPUT_DIR = Path(__file__).resolve().parent

TEXT_OUTPUT_PATH = OUTPUT_DIR / "comparison_50_questions.txt"
METADATA_OUTPUT_PATH = OUTPUT_DIR / "comparison_50_metadata.csv"
PROVENANCE_OUTPUT_PATH = OUTPUT_DIR / "comparison_50_provenance.json"


# ---------------------------------------------------------------------------
# Comparison/ranking classification
# ---------------------------------------------------------------------------

# HiTab aggregation operators that directly encode comparison, selection,
# ordering, or threshold reasoning.
COMPARISON_OPERATORS = {
    "argmax",
    "argmin",
    "greater_than",
    "kth-argmax",
    "less_than",
    "max",
    "min",
    "pair-argmax",
    "pair-argmin",
    "topk-argmax",
}


# Manual audit of questions carrying a comparison operator but whose actual
# question is not a comparison/ranking task.
#
# These exclusions are recorded explicitly so the construction of the
# candidate pool can be reproduced rather than relying on undocumented
# human decisions.
MANUAL_EXCLUSIONS = {
    "4ee3dc8ad6611cc2d74b85ee1eb95ade": (
        "asks for the size of a decline between two cohorts; the requested "
        "answer is an arithmetic difference, not a selection or ranking"
    ),
    "38dfac9974573af3c7f8ba67fd55c4fb": (
        "asks for one stated proportion for Aboriginal men, so it is a "
        "direct lookup"
    ),
    "dc983b8c08626cb1212080258fb7dca1": (
        "question text is malformed and contains only ['2016']"
    ),
    "606100b41d36085b1ef6634b931dfaef": (
        "asks for the percentage at one named row/column intersection, "
        "so it is a direct lookup"
    ),
    "02250bf4078191f9c34f27df963fb6b1": (
        "asks for a heat rank already printed in the table, so it is a "
        "direct lookup"
    ),
    "9d39b47e27e0ed95fcb3c23b7dd5acb2": (
        "asks which competitions Monaco participated in; it is a list "
        "lookup rather than a ranking"
    ),
}


# Manual audit of questions without one of the comparison operators above
# whose semantics nevertheless require comparison/ranking reasoning.
MANUAL_INCLUSIONS = {
    "28f3628abf672ac0297baa46b2a6253c": (
        "requires finding the maximum Quebec French-speaker projection "
        "across the 2036 scenarios"
    ),
    "90e88d3b6bbd41be6c41cd82b95d1333": (
        "requires comparing unmet-need percentages across need types"
    ),
    "e0b9336f29edb3db7d7fba39bffc2b96": (
        "requires comparing fraud-rate changes across census metropolitan "
        "areas"
    ),
    "c8ca6545aec2ed94ab51446f7f7b1510": (
        "requires comparing sector-level Canada-US wage-growth gaps with "
        "a 15-point threshold"
    ),
    "1c2e392b266e6c1f3e11d47e6d803e2e": (
        "requires finding the supervision type with the lowest female "
        "admission percentage"
    ),
    "37946b67576753881c93608a536d25cc": (
        "requires finding the age group with the maximum 2003 vaccination "
        "rate"
    ),
    "a49aedf0036c8c9bc5b32b5705a9e92c": (
        "requires ranking police services and selecting the ten highest rates"
    ),
    "744d9e14f23ff650bfd218711911730f": (
        "requires finding the occupation with the highest men's share among "
        "all workers"
    ),
    "0768f450f1df339f90577ade7a66e78f": (
        "requires finding the occupation with the highest women's share "
        "among all workers"
    ),
    "ba49822ee491a40f8dcd070e921a26f6": (
        "requires comparing each region's farm-computer/internet use with "
        "the Quebec total"
    ),
    "e586d5f09c789ec09384d6450c69419c": (
        "requires comparing the headcounts of two owner types"
    ),
}


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def sha256_file(path: Path) -> str:
    """Return the SHA-256 digest of a file."""

    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def check_source_files() -> None:
    """Verify that the required HiTab files are available."""

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Missing HiTab test file:\n{DATASET_PATH}\n\n"
            "Expected the HiTab quality-checked test split at "
            f"{DATASET_RELATIVE_PATH}."
        )

    if not TABLE_ARCHIVE_PATH.exists():
        raise FileNotFoundError(
            f"Missing HiTab table archive:\n{TABLE_ARCHIVE_PATH}\n\n"
            "Expected tables.zip at "
            f"{TABLE_ARCHIVE_RELATIVE_PATH}."
        )


# ---------------------------------------------------------------------------
# Load dataset
# ---------------------------------------------------------------------------

def load_samples() -> list[dict[str, Any]]:
    """Load the HiTab quality-checked test questions."""

    with DATASET_PATH.open(encoding="utf-8") as handle:
        samples = [
            json.loads(line)
            for line in handle
            if line.strip()
        ]

    ids = [sample["id"] for sample in samples]

    if len(ids) != len(set(ids)):
        raise ValueError(
            "The source test file contains duplicate question IDs."
        )

    return samples


# ---------------------------------------------------------------------------
# Candidate classification
# ---------------------------------------------------------------------------

def is_comparison_candidate(sample: dict[str, Any]) -> bool:
    """
    Return True if a question belongs in the comparison/ranking pool.
    """

    question_id = sample["id"]

    if question_id in MANUAL_EXCLUSIONS:
        return False

    if question_id in MANUAL_INCLUSIONS:
        return True

    aggregation = sample.get("aggregation") or []

    return bool(
        COMPARISON_OPERATORS.intersection(aggregation)
    )


# ---------------------------------------------------------------------------
# Sample selection
# ---------------------------------------------------------------------------

def select_samples(
    samples: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Construct the audited comparison/ranking pool and draw the fixed
    50-question sample.
    """

    candidates = sorted(
        (
            sample
            for sample in samples
            if is_comparison_candidate(sample)
        ),
        key=lambda sample: sample["id"],
    )

    if len(candidates) < SAMPLE_SIZE:
        raise RuntimeError(
            f"Only {len(candidates)} comparison/ranking candidates "
            f"are available; at least {SAMPLE_SIZE} are required."
        )

    selected = random.Random(SEED).sample(
        candidates,
        SAMPLE_SIZE,
    )

    return selected, candidates


# ---------------------------------------------------------------------------
# Load tables
# ---------------------------------------------------------------------------

def load_selected_tables(
    selected: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """
    Load the raw HiTab tables corresponding to the selected questions.
    """

    tables: dict[str, dict[str, Any]] = {}

    with zipfile.ZipFile(TABLE_ARCHIVE_PATH) as archive:
        archive_names = set(archive.namelist())

        for sample in selected:
            table_id = str(sample["table_id"])

            member = f"tables/raw/{table_id}.json"

            if member not in archive_names:
                raise FileNotFoundError(
                    f"No raw table JSON for table_id={table_id}. "
                    f"Expected archive member: {member}"
                )

            table = json.loads(
                archive.read(member).decode("utf-8")
            )

            texts = table.get("texts")

            if not isinstance(texts, list) or not texts:
                raise ValueError(
                    f"Table {table_id} has no visible rows in 'texts'."
                )

            if any(
                not isinstance(row, list)
                for row in texts
            ):
                raise ValueError(
                    f"Table {table_id} contains an invalid row."
                )

            tables[table_id] = table

    return tables


# ---------------------------------------------------------------------------
# Table rendering
# ---------------------------------------------------------------------------

def render_cell(
    column_number: int,
    value: Any,
) -> str:
    """Render one table cell with its zero-based column coordinate."""

    if value is None:
        text = ""
    elif isinstance(value, str):
        text = value
    else:
        text = str(value)

    # Physical newlines would break the one-row-per-line representation.
    if "\n" in text or "\r" in text:
        raise ValueError(
            f"Cell [{column_number}] contains a newline and cannot "
            "be serialized faithfully."
        )

    if text == "":
        return f"[{column_number}]"

    return f"[{column_number}] {text}"


def render_block(
    sample_index: int,
    sample: dict[str, Any],
    table: dict[str, Any],
) -> str:
    """Render one question and its complete table."""

    lines = [
        f"=== QUESTION {sample_index} ===",
        "",
        f"question_id: {sample['id']}",
        "",
        f"table_id: {sample['table_id']}",
        "",
        f"Table title: {table.get('title', '')}",
        "",
        (
            "Table (cells are written as [column] value; "
            "row and column numbers start at 0 and count header rows):"
        ),
        "",
    ]

    for row_number, row in enumerate(table["texts"]):
        cells = " | ".join(
            render_cell(column_number, value)
            for column_number, value in enumerate(row)
        )

        lines.append(
            f"Row {row_number}: {cells}"
        )

    lines.extend(
        [
            "",
            f"Question: {sample['question']}",
        ]
    )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Write outputs
# ---------------------------------------------------------------------------

def write_outputs(
    selected: list[dict[str, Any]],
    tables: dict[str, dict[str, Any]],
) -> str:
    """Write model input and sample metadata."""

    blocks = [
        render_block(
            index,
            sample,
            tables[str(sample["table_id"])],
        )
        for index, sample in enumerate(selected, 1)
    ]

    text_output = "\n\n".join(blocks) + "\n"

    TEXT_OUTPUT_PATH.write_text(
        text_output,
        encoding="utf-8",
    )

    fieldnames = [
        "sample_index",
        "question_id",
        "table_id",
        "split",
        "dataset_file",
        "dataset_revision",
        "selection_seed",
        "classification",
        "question",
        "answer",
        "aggregation",
        "table_title",
    ]

    with METADATA_OUTPUT_PATH.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for index, sample in enumerate(selected, 1):
            table = tables[str(sample["table_id"])]

            writer.writerow(
                {
                    "sample_index": index,
                    "question_id": sample["id"],
                    "table_id": sample["table_id"],
                    "split": "test",
                    "dataset_file": DATASET_RELATIVE_PATH,
                    "dataset_revision": DATASET_REVISION,
                    "selection_seed": SEED,
                    "classification": CLASSIFICATION,
                    "question": sample["question"],
                    "answer": json.dumps(
                        sample.get("answer"),
                        ensure_ascii=False,
                    ),
                    "aggregation": json.dumps(
                        sample.get("aggregation") or [],
                        ensure_ascii=False,
                    ),
                    "table_title": table.get("title", ""),
                }
            )

    return text_output


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_outputs(
    selected: list[dict[str, Any]],
    tables: dict[str, dict[str, Any]],
    text_output: str,
) -> None:
    """Validate the generated 50-question model input."""

    if len(selected) != SAMPLE_SIZE:
        raise AssertionError(
            f"Expected {SAMPLE_SIZE} questions; "
            f"found {len(selected)}."
        )

    selected_ids = [
        sample["id"]
        for sample in selected
    ]

    if len(selected_ids) != len(set(selected_ids)):
        raise AssertionError(
            "Selected question IDs are not unique."
        )

    if any(
        not is_comparison_candidate(sample)
        for sample in selected
    ):
        raise AssertionError(
            "At least one selected question is outside "
            "the audited comparison/ranking candidate pool."
        )

    missing_tables = (
        set(
            str(sample["table_id"])
            for sample in selected
        )
        - set(tables)
    )

    if missing_tables:
        raise AssertionError(
            f"Missing selected tables: {sorted(missing_tables)}"
        )

    # Confirm that exactly 50 question blocks were written.
    blocks = re.split(
        r"(?=^=== QUESTION \d+ ===$)",
        text_output,
        flags=re.MULTILINE,
    )

    blocks = [
        block
        for block in blocks
        if block.strip()
    ]

    if len(blocks) != SAMPLE_SIZE:
        raise AssertionError(
            f"Expected {SAMPLE_SIZE} serialized blocks; "
            f"found {len(blocks)}."
        )

    # Make sure hidden HiTab supervision was not explicitly serialized
    # into the model input.
    forbidden_metadata = (
        "\nanswer:",
        "\naggregation:",
        "\nlinked_cells:",
        "\nanswer_formulas:",
        "\nreference_cells_map:",
    )

    lowered_output = text_output.lower()

    if any(
        label in lowered_output
        for label in forbidden_metadata
    ):
        raise AssertionError(
            "Gold supervision appears in the model input."
        )

    # Confirm that each table was serialized completely and faithfully.
    for index, (sample, block) in enumerate(
        zip(selected, blocks),
        1,
    ):
        table = tables[str(sample["table_id"])]

        required_fragments = (
            f"=== QUESTION {index} ===",
            f"question_id: {sample['id']}",
            f"table_id: {sample['table_id']}",
            "Table title:",
            "Row 0: [0]",
            f"Question: {sample['question']}",
        )

        for fragment in required_fragments:
            if fragment not in block:
                raise AssertionError(
                    f"Question block {index} is missing: "
                    f"{fragment}"
                )

        row_lines = [
            line
            for line in block.splitlines()
            if line.startswith("Row ")
        ]

        if len(row_lines) != len(table["texts"]):
            raise AssertionError(
                f"Question block {index} does not contain "
                "the complete source table."
            )

        for row_number, (
            rendered_line,
            source_row,
        ) in enumerate(
            zip(row_lines, table["texts"])
        ):
            expected_cells = " | ".join(
                render_cell(column_number, value)
                for column_number, value
                in enumerate(source_row)
            )

            expected_line = (
                f"Row {row_number}: {expected_cells}"
            )

            if rendered_line != expected_line:
                raise AssertionError(
                    f"Question {index}, row {row_number} "
                    "differs from the source table."
                )


# ---------------------------------------------------------------------------
# Provenance
# ---------------------------------------------------------------------------

def write_provenance(
    samples: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    selected: list[dict[str, Any]],
) -> None:
    """
    Record information needed to verify exactly which source files and
    sampling configuration produced the evaluation set.
    """

    provenance = {
        "dataset": "HiTab",
        "dataset_revision": DATASET_REVISION,
        "dataset_file": DATASET_RELATIVE_PATH,
        "dataset_sha256": sha256_file(DATASET_PATH),
        "table_archive": TABLE_ARCHIVE_RELATIVE_PATH,
        "table_archive_sha256": sha256_file(
            TABLE_ARCHIVE_PATH
        ),
        "source_question_count": len(samples),
        "comparison_candidate_count": len(candidates),
        "sample_size": SAMPLE_SIZE,
        "selection_seed": SEED,
        "classification": CLASSIFICATION,
        "python_version": platform.python_version(),
        "selected_question_ids": [
            sample["id"]
            for sample in selected
        ],
        "manual_exclusions": MANUAL_EXCLUSIONS,
        "manual_inclusions": MANUAL_INCLUSIONS,
    }

    PROVENANCE_OUTPUT_PATH.write_text(
        json.dumps(
            provenance,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    check_source_files()

    samples = load_samples()

    selected, candidates = select_samples(samples)

    tables = load_selected_tables(selected)

    text_output = write_outputs(
        selected,
        tables,
    )

    validate_outputs(
        selected,
        tables,
        text_output,
    )

    write_provenance(
        samples,
        candidates,
        selected,
    )

    print("VALIDATION: PASS")
    print(f"dataset_revision: {DATASET_REVISION}")
    print(f"source_questions: {len(samples)}")
    print(
        f"comparison_ranking_candidates: "
        f"{len(candidates)}"
    )
    print(f"selection_seed: {SEED}")
    print(f"selected_questions: {len(selected)}")

    print(
        f"questions_output: "
        f"{TEXT_OUTPUT_PATH.relative_to(REPO_ROOT)}"
    )

    print(
        f"metadata_output: "
        f"{METADATA_OUTPUT_PATH.relative_to(REPO_ROOT)}"
    )

    print(
        f"provenance_output: "
        f"{PROVENANCE_OUTPUT_PATH.relative_to(REPO_ROOT)}"
    )


if __name__ == "__main__":
    main()
