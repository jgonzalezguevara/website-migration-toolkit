import json
from pathlib import Path
from typing import Any


def write_json(
    destination: Path,
    data: Any,
) -> None:
    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with destination.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
            sort_keys=True,
        )
