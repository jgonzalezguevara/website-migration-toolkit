from collections.abc import Iterable

from migration.models.comparison import ComparisonItem
from migration.models.inventory import InventoryItem


def compare_inventories(
    old_inventory: Iterable[InventoryItem],
    new_inventory: Iterable[InventoryItem],
) -> list[ComparisonItem]:
    old_items = {
        item.path: item
        for item in old_inventory
    }

    new_items = {
        item.path: item
        for item in new_inventory
    }

    paths = sorted(
        set(old_items) | set(new_items)
    )

    comparison = []

    for path in paths:
        old_item = old_items.get(path)
        new_item = new_items.get(path)

        if old_item is None and new_item is not None:
            comparison.append(
                ComparisonItem(
                    path=path,
                    status="added",
                    new_extension=new_item.extension,
                    new_category=new_item.category,
                    new_size=new_item.size,
                    size_difference=new_item.size,
                    new_sha256=new_item.sha256 or "",
                )
            )
            continue

        if old_item is not None and new_item is None:
            comparison.append(
                ComparisonItem(
                    path=path,
                    status="removed",
                    old_extension=old_item.extension,
                    old_category=old_item.category,
                    old_size=old_item.size,
                    size_difference=-old_item.size,
                    old_sha256=old_item.sha256 or "",
                )
            )
            continue

        if old_item is None or new_item is None:
            continue

        changed = (
            old_item.extension != new_item.extension
            or old_item.category != new_item.category
            or old_item.size != new_item.size
            or (
                old_item.sha256 is not None
                and new_item.sha256 is not None
                and old_item.sha256 != new_item.sha256
            )
        )

        comparison.append(
            ComparisonItem(
                path=path,
                status=(
                    "modified"
                    if changed
                    else "unchanged"
                ),
                old_extension=old_item.extension,
                new_extension=new_item.extension,
                old_category=old_item.category,
                new_category=new_item.category,
                old_size=old_item.size,
                new_size=new_item.size,
                size_difference=(
                    new_item.size - old_item.size
                ),
                old_sha256=old_item.sha256 or "",
                new_sha256=new_item.sha256 or "",
            )
        )

    return comparison
