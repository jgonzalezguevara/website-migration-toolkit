import json
import shutil
from collections import Counter
from html import escape
from pathlib import Path
from string import Template
from typing import Iterable

from migration.models.discovery import Page
from migration.models.inventory import InventoryItem
from migration.models.mapping import MigrationMapItem
from migration.models.validation import ValidationIssue
from migration.reporting.statistics import build_statistics


TEMPLATE_DIRECTORY = (
    Path(__file__).parent / "templates"
)


def format_size(size: int) -> str:
    units = [
        "B",
        "KB",
        "MB",
        "GB",
        "TB",
    ]

    value = float(size)

    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"

            return f"{value:.2f} {unit}"

        value /= 1024

    return f"{size} B"


def build_issue_rows(
    issues: Iterable[ValidationIssue],
) -> str:
    rows = []

    for issue in issues:
        severity = escape(
            issue.severity.lower()
        )

        rows.append(
            "\n".join(
                [
                    "<tr>",
                    "  <td>",
                    (
                        f'    <span class="severity '
                        f'severity-{severity}">'
                        f"{escape(issue.severity)}"
                        "</span>"
                    ),
                    "  </td>",
                    (
                        f"  <td>{escape(issue.validator)}</td>"
                    ),
                    (
                        f"  <td>{escape(issue.type)}</td>"
                    ),
                    (
                        f"  <td>{escape(issue.source)}</td>"
                    ),
                    (
                        f"  <td>{escape(issue.target)}</td>"
                    ),
                    (
                        f"  <td>{escape(issue.message)}</td>"
                    ),
                    "</tr>",
                ]
            )
        )

    if not rows:
        return (
            '<tr><td colspan="6" class="empty-state">'
            "No validation issues found"
            "</td></tr>"
        )

    return "\n".join(rows)


def build_migration_status(
    mapping: Iterable[MigrationMapItem],
) -> dict[str, int]:
    counts = Counter(
        item.status
        for item in mapping
    )

    return dict(
        sorted(counts.items())
    )


def write_dashboard(
    destination: Path,
    pages: Iterable[Page],
    inventory: Iterable[InventoryItem],
    issues: Iterable[ValidationIssue],
    mapping: Iterable[MigrationMapItem],
) -> Path:
    page_items = list(pages)
    inventory_items = list(inventory)
    issue_items = list(issues)
    mapping_items = list(mapping)

    statistics = build_statistics(
        inventory_items,
        issue_items,
    )

    template_path = (
        TEMPLATE_DIRECTORY / "dashboard.html"
    )

    css_source = (
        TEMPLATE_DIRECTORY / "dashboard.css"
    )

    javascript_source = (
        TEMPLATE_DIRECTORY / "dashboard.js"
    )

    if not template_path.exists():
        raise FileNotFoundError(
            f"No existe la plantilla: {template_path}"
        )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    template = Template(
        template_path.read_text(
            encoding="utf-8",
        )
    )

    inventory_statistics = statistics[
        "inventory"
    ]

    validation_statistics = statistics[
        "validation"
    ]

    rendered = template.safe_substitute(
        generated_at=escape(
            statistics["generated_at"]
        ),
        total_pages=len(page_items),
        total_files=inventory_statistics[
            "total_files"
        ],
        total_size=format_size(
            inventory_statistics[
                "total_size_bytes"
            ]
        ),
        total_issues=validation_statistics[
            "total_issues"
        ],
        files_by_category=escape(
            json.dumps(
                inventory_statistics[
                    "files_by_category"
                ],
                ensure_ascii=False,
            ),
            quote=True,
        ),
        issues_by_severity=escape(
            json.dumps(
                validation_statistics[
                    "issues_by_severity"
                ],
                ensure_ascii=False,
            ),
            quote=True,
        ),
        issues_by_validator=escape(
            json.dumps(
                validation_statistics[
                    "issues_by_validator"
                ],
                ensure_ascii=False,
            ),
            quote=True,
        ),
        migration_status=escape(
            json.dumps(
                build_migration_status(
                    mapping_items
                ),
                ensure_ascii=False,
            ),
            quote=True,
        ),
        issues_rows=build_issue_rows(
            issue_items
        ),
    )

    destination.write_text(
        rendered,
        encoding="utf-8",
    )

    shutil.copyfile(
        css_source,
        destination.parent / "dashboard.css",
    )

    shutil.copyfile(
        javascript_source,
        destination.parent / "dashboard.js",
    )

    return destination
