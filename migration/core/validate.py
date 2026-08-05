from migration.validators.links import validate as validate_links
from migration.validators.pages import validate as validate_pages
from migration.validators.resources import validate as validate_resources


VALIDATORS = (
    validate_links,
    validate_pages,
    validate_resources,
)


def run_validation(pages, links, resources, source_root=None):
    issues = []

    for validator in VALIDATORS:
        issues.extend(
            validator(
                pages,
                links,
                resources,
                source_root,
            )
        )

    return issues
