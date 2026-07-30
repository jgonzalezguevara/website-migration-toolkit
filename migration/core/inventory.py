from datetime import datetime, timezone

from pathlib import Path

from migration.models.inventory import (
    InventoryItem,
    classify_file,
)
from migration.reporting.csv import write_csv
from migration.utils.filesystem import find_files


def build_inventory(
    root: Path,
    output: Path | None = None,
) -> list[InventoryItem]:

    inventory = []

    for file in find_files(root):

        stat = file.stat()

        inventory.append(
            InventoryItem(
                path=str(file.relative_to(root)),
                extension=file.suffix.lower(),
                category=classify_file(file),
                size=stat.st_size,
                modified_at=stat.st_mtime,
                modified_iso=datetime.fromtimestamp(
                    stat.st_mtime,
                    tz=timezone.utc,
                ).isoformat(),
            )
        )

    if output is not None:
        write_csv(
            output / "inventory.csv",
            inventory,
        )

    return inventory
