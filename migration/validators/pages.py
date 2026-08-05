from migration.models.validation import ValidationIssue


def validate(pages, links, resources, source_root=None):
    issues = []

    for page in pages:
        if page.empty:
            issues.append(
                ValidationIssue(
                    validator="pages",
                    severity="error",
                    type="empty-page",
                    source=page.file,
                    target=page.inferred_route or "",
                    message="Empty HTML page",
                )
            )

        if page.appears_404:
            issues.append(
                ValidationIssue(
                    validator="pages",
                    severity="warning",
                    type="possible-404-page",
                    source=page.file,
                    target=page.inferred_route or "",
                    message="Page appears to contain a 404 response",
                )
            )

    return issues
