from migration.models.validation import ValidationIssue


def validate(
    pages,
    links,
    resources,
    source_root=None,
):
    issues = []

    for page in pages:
        target = page.inferred_route or ""

        if not page.canonical:
            issues.append(
                ValidationIssue(
                    validator="seo",
                    severity="warning",
                    type="missing-canonical",
                    source=page.file,
                    target=target,
                    message="Page has no canonical URL",
                )
            )

        elif not page.canonical.startswith(
            ("http://", "https://")
        ):
            issues.append(
                ValidationIssue(
                    validator="seo",
                    severity="warning",
                    type="relative-canonical",
                    source=page.file,
                    target=page.canonical,
                    message="Canonical URL is relative",
                )
            )

        robots = page.robots.casefold()

        if "noindex" in robots:
            issues.append(
                ValidationIssue(
                    validator="seo",
                    severity="warning",
                    type="noindex-page",
                    source=page.file,
                    target=target,
                    message="Page is marked as noindex",
                )
            )

        if not page.title.strip():
            issues.append(
                ValidationIssue(
                    validator="seo",
                    severity="error",
                    type="missing-title",
                    source=page.file,
                    target=target,
                    message="Page has no title",
                )
            )

        elif len(page.title) > 60:
            issues.append(
                ValidationIssue(
                    validator="seo",
                    severity="warning",
                    type="long-title",
                    source=page.file,
                    target=target,
                    message="Page title exceeds 60 characters",
                )
            )

        if not page.meta_description.strip():
            issues.append(
                ValidationIssue(
                    validator="seo",
                    severity="warning",
                    type="missing-meta-description",
                    source=page.file,
                    target=target,
                    message="Page has no meta description",
                )
            )

        elif len(page.meta_description) > 160:
            issues.append(
                ValidationIssue(
                    validator="seo",
                    severity="warning",
                    type="long-meta-description",
                    source=page.file,
                    target=target,
                    message="Meta description exceeds 160 characters",
                )
            )

        if page.h1_count == 0:
            issues.append(
                ValidationIssue(
                    validator="seo",
                    severity="warning",
                    type="missing-h1",
                    source=page.file,
                    target=target,
                    message="Page has no H1 heading",
                )
            )

        elif page.h1_count > 1:
            issues.append(
                ValidationIssue(
                    validator="seo",
                    severity="warning",
                    type="multiple-h1",
                    source=page.file,
                    target=target,
                    message="Page has multiple H1 headings",
                )
            )

    titles = {}
    descriptions = {}

    for page in pages:
        title = page.title.strip()

        if title:
            titles.setdefault(
                title.casefold(),
                [],
            ).append(page)

        description = page.meta_description.strip()

        if description:
            descriptions.setdefault(
                description.casefold(),
                [],
            ).append(page)

    for duplicated_pages in titles.values():
        if len(duplicated_pages) < 2:
            continue

        for page in duplicated_pages:
            issues.append(
                ValidationIssue(
                    validator="seo",
                    severity="warning",
                    type="duplicate-title",
                    source=page.file,
                    target=page.inferred_route or "",
                    message="Page title is duplicated",
                )
            )

    for duplicated_pages in descriptions.values():
        if len(duplicated_pages) < 2:
            continue

        for page in duplicated_pages:
            issues.append(
                ValidationIssue(
                    validator="seo",
                    severity="warning",
                    type="duplicate-meta-description",
                    source=page.file,
                    target=page.inferred_route or "",
                    message="Meta description is duplicated",
                )
            )

    return issues
