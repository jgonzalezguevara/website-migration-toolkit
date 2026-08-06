import csv
from pathlib import Path

from migration.models.inventory import InventoryItem


def read_inventory_csv(
    source: Path,
) -> list[InventoryItem]:
    if not source.exists():
        raise FileNotFoundError(
            f"No existe el inventario: {source}"
        )

    items = []

    with source.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            items.append(
                InventoryItem(
                    path=row["path"],
                    extension=row["extension"],
                    category=row["category"],
                    size=int(row["size"]),
                    modified_at=float(
                        row["modified_at"]
                    ),
                    modified_iso=row["modified_iso"],
                    sha256=(
                        row.get("sha256")
                        or None
                    ),
                )
            )

    return items
