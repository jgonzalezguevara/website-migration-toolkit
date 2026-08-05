from migration.validators.links import validate as validate_links


VALIDATORS = (
    validate_links,
)


def run_validation(pages, links, resources):
    issues = []

    for validator in VALIDATORS:
        issues.extend(
            validator(
                pages,
                links,
                resources,
            )
        )

    return issues
