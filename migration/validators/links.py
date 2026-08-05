from migration.models.validation import ValidationIssue


def validate(pages, links, resources, source_root=None):
    issues = []
    seen = set()

    existing_routes = {
        page.inferred_route
        for page in pages
        if page.inferred_route
    }

    ignored_prefixes = (
        "http://",
        "https://",
        "mailto:",
        "tel:",
        "javascript:",
        "#",
    )

    for link in links:

        if not link.href:
            continue

        if link.href.startswith(ignored_prefixes):
            continue

        if not link.normalized_route:
            continue

        if link.normalized_route in existing_routes:
            continue

        key = (
            link.source_file,
            link.normalized_route,
        )

        if key in seen:
            continue

        seen.add(key)

        issues.append(
            ValidationIssue(
                validator="links",
                severity="error",
                type="broken-link",
                source=link.source_file,
                target=link.href,
                message="Broken internal link",
            )
        )

    return issues
