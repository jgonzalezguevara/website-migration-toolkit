import csv
from dataclasses import asdict
from pathlib import Path
from typing import Iterable


def write_csv(
    destination: Path,
    rows: Iterable,
) -> None:

    items = list(rows)

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not items:
        destination.write_text(
            "",
            encoding="utf-8",
        )
        return

    dictionaries = [
        asdict(item)
        if not isinstance(item, dict)
        else item
        for item in items
    ]

    with destination.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=dictionaries[0].keys(),
        )

        writer.writeheader()
        writer.writerows(dictionaries)
