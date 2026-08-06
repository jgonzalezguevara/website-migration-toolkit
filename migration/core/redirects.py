import csv
from pathlib import Path


def load_redirects(path: Path | None) -> dict[str, str]:
    if path is None or not path.exists():
        return {}

    redirects = {}

    with path.open(
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            source = (
                row.get("old_route", "")
                .strip()
            )
            target = (
                row.get("new_route", "")
                .strip()
            )

            if source and target:
                redirects[source] = target

    return redirects
