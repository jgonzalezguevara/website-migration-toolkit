from collections import Counter
from pathlib import Path


def write_validation_markdown(
    path: Path,
    issues,
) -> None:
    by_severity = Counter(
        issue.severity
        for issue in issues
    )

    by_type = Counter(
        issue.type
        for issue in issues
    )

    lines = [
        "# Validation report",
        "",
        "## Summary",
        "",
        f"- Total issues: {len(issues)}",
    ]

    for severity, count in sorted(
        by_severity.items()
    ):
        lines.append(
            f"- {severity}: {count}"
        )

    lines.extend([
        "",
        "## Issue types",
        "",
    ])

    for issue_type, count in sorted(
        by_type.items()
    ):
        lines.append(
            f"- {issue_type}: {count}"
        )

    lines.extend([
        "",
        "## Issues",
        "",
        "| Severity | Type | Source | Target | Message |",
        "|----------|------|--------|--------|---------|",
    ])

    for issue in issues:
        lines.append(
            f"| {issue.severity} | "
            f"{issue.type} | "
            f"{issue.source} | "
            f"{issue.target} | "
            f"{issue.message} |"
        )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )
