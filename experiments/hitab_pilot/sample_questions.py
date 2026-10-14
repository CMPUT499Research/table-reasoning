"""Create a reproducible HiTab development-question registry."""

import argparse
import csv
import json
import random
from pathlib import Path


DATASET_REVISION = "d179602662b490249baf068a76fbe4137029126e"
DATASET_FILE = "data/dev_samples.jsonl"
SEED = 499
SAMPLE_SIZE = 30

FIELDNAMES = [
    "sample_id",
    "table_id",
    "split",
    "dataset_file",
    "dataset_revision",
    "selection_seed",
    "question",
    "table_source",
    "table_serialization_version",
    "notes",
]


def read_examples(path: Path) -> list[dict]:
    """Read non-empty JSONL lines into a list of question records."""
    with path.open(encoding="utf-8") as source:
        return [
            json.loads(line)
            for line in source
            if line.strip()
        ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_jsonl", type=Path)
    parser.add_argument("output_csv", type=Path)
    arguments = parser.parse_args()

    examples = sorted(
        read_examples(arguments.input_jsonl),
        key=lambda example: example["id"],
    )

    if len(examples) < SAMPLE_SIZE:
        raise ValueError(
            f"Expected at least {SAMPLE_SIZE} examples; "
            f"found {len(examples)}."
        )

    question_ids = [example["id"] for example in examples]
    if len(question_ids) != len(set(question_ids)):
        raise ValueError("Duplicate question IDs found in the input file.")

    selected_examples = random.Random(SEED).sample(
        examples,
        SAMPLE_SIZE,
    )

    arguments.output_csv.parent.mkdir(parents=True, exist_ok=True)

    with arguments.output_csv.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as destination:
        writer = csv.DictWriter(
            destination,
            fieldnames=FIELDNAMES,
            lineterminator="\n",
        )
        writer.writeheader()

        for example in selected_examples:
            writer.writerow(
                {
                    "sample_id": example["id"],
                    "table_id": example["table_id"],
                    "split": "dev",
                    "dataset_file": DATASET_FILE,
                    "dataset_revision": DATASET_REVISION,
                    "selection_seed": SEED,
                    "question": example["question"],
                    "table_source": example["table_source"],
                    "table_serialization_version": "not_implemented",
                    "notes": "",
                }
            )


if __name__ == "__main__":
    main()