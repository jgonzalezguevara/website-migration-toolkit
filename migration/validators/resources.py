from pathlib import Path
from urllib.parse import urlparse

from migration.models.validation import ValidationIssue


def validate(
    pages,
    links,
    resources,
    source_root=None,
):
    issues = []
    seen = set()

    if source_root is None:
        return issues

    source_root = Path(source_root)

    for resource in resources:
        if resource.type == "form":
            continue

        value = (resource.value or "").strip()

        if not value:
            continue

        parsed = urlparse(value)

        if parsed.scheme or parsed.netloc:
            continue

        if value.startswith(
            (
                "#",
                "data:",
                "mailto:",
                "tel:",
                "javascript:",
            )
        ):
            continue

        clean_path = parsed.path

        if clean_path.startswith("/"):
            candidate = (
                source_root
                / clean_path.lstrip("/")
            )
        else:
            source_dir = Path(
                resource.source_file
            ).parent

            candidate = (
                source_root
                / source_dir
                / clean_path
            )

        candidate = candidate.resolve()

        try:
            candidate.relative_to(
                source_root.resolve()
            )
        except ValueError:
            continue

        if candidate.exists():
            continue

        key = (
            resource.source_file,
            resource.type,
            value,
        )

        if key in seen:
            continue

        seen.add(key)

        issues.append(
            ValidationIssue(
                validator="resources",
                severity="error",
                type="missing-resource",
                source=resource.source_file,
                target=value,
                message=(
                    f"Missing local {resource.type}"
                ),
            )
        )

    return issues
