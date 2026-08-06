from collections import Counter
from datetime import datetime, timezone
from typing import Iterable

from migration.models.inventory import InventoryItem
from migration.models.validation import ValidationIssue


def build_statistics(
    inventory: Iterable[InventoryItem],
    issues: Iterable[ValidationIssue],
) -> dict:

    inventory_items = list(inventory)
    validation_issues = list(issues)

    files_by_category = Counter(
        item.category
        for item in inventory_items
    )

    files_by_extension = Counter(
        item.extension or "[no extension]"
        for item in inventory_items
    )

    issues_by_severity = Counter(
        issue.severity
        for issue in validation_issues
    )

    issues_by_type = Counter(
        issue.type
        for issue in validation_issues
    )

    issues_by_validator = Counter(
        issue.validator
        for issue in validation_issues
    )

    total_size = sum(
        item.size
        for item in inventory_items
    )

    return {
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "inventory": {
            "total_files": len(inventory_items),
            "total_size_bytes": total_size,
            "files_by_category": dict(
                sorted(files_by_category.items())
            ),
            "files_by_extension": dict(
                sorted(files_by_extension.items())
            ),
        },
        "validation": {
            "total_issues": len(validation_issues),
            "issues_by_severity": dict(
                sorted(issues_by_severity.items())
            ),
            "issues_by_type": dict(
                sorted(issues_by_type.items())
            ),
            "issues_by_validator": dict(
                sorted(issues_by_validator.items())
            ),
        },
    }
