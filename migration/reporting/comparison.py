from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from migration.models.comparison import ComparisonItem
from migration.reporting.csv import write_csv
from migration.reporting.json import write_json


def build_comparison_summary(
    items: Iterable[ComparisonItem],
) -> dict:
    comparison_items = list(items)

    status_counts = Counter(
        item.status
        for item in comparison_items
    )

    total_size_difference = sum(
        item.size_difference
        for item in comparison_items
    )

    return {
        "total_items": len(comparison_items),
        "status": dict(
            sorted(status_counts.items())
        ),
        "total_size_difference": (
            total_size_difference
        ),
    }


def write_comparison_markdown(
    destination: Path,
    items: Iterable[ComparisonItem],
) -> Path:
    comparison_items = list(items)

    summary = build_comparison_summary(
        comparison_items
    )

    lines = [
        "# Website comparison report",
        "",
        "## Summary",
        "",
        f"- Total items: {summary['total_items']}",
    ]

    for status, count in summary["status"].items():
        lines.append(
            f"- {status}: {count}"
        )

    lines.extend(
        [
            (
                "- Total size difference: "
                f"{summary['total_size_difference']} bytes"
            ),
            "",
            "## Files",
            "",
            (
                "| Path | Status | Old category | "
                "New category | Old size | New size | "
                "Difference |"
            ),
            (
                "|------|--------|--------------|"
                "--------------|----------|----------|"
                "------------|"
            ),
        ]
    )

    for item in comparison_items:
        lines.append(
            (
                f"| {item.path} "
                f"| {item.status} "
                f"| {item.old_category} "
                f"| {item.new_category} "
                f"| {item.old_size} "
                f"| {item.new_size} "
                f"| {item.size_difference} |"
            )
        )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    return destination


def write_comparison_reports(
    output_directory: Path,
    items: Iterable[ComparisonItem],
) -> dict[str, Path]:
    comparison_items = list(items)

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    csv_path = (
        output_directory / "comparison.csv"
    )

    json_path = (
        output_directory / "comparison.json"
    )

    markdown_path = (
        output_directory / "comparison.md"
    )

    write_csv(
        csv_path,
        comparison_items,
    )

    write_json(
        json_path,
        {
            "summary": build_comparison_summary(
                comparison_items
            ),
            "items": [
                asdict(item)
                for item in comparison_items
            ],
        },
    )

    write_comparison_markdown(
        markdown_path,
        comparison_items,
    )

    return {
        "csv": csv_path,
        "json": json_path,
        "markdown": markdown_path,
    }
