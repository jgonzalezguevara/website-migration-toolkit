from migration.validators.loader import load_validators


def run_validation(
    pages,
    links,
    resources,
    source_root=None,
):
    issues = []

    for validator in load_validators():
        issues.extend(
            validator(
                pages,
                links,
                resources,
                source_root,
            )
        )

    return issues
