from urllib.parse import unquote

from migration.models.validation import ValidationIssue


def validate(
    pages,
    links,
    resources,
    source_root=None,
):
    issues = []
    seen = set()

    for resource in resources:
        if resource.type != "image":
            continue

        if resource.alt.strip():
            continue

        normalized = unquote(
            resource.value.strip()
        ).lstrip("/")

        if not normalized:
            continue

        if normalized in seen:
            continue

        seen.add(normalized)

        issues.append(
            ValidationIssue(
                validator="images",
                severity="warning",
                type="missing-alt",
                source=resource.source_file,
                target=resource.value,
                message="Image has no alt text",
            )
        )

    return issues
