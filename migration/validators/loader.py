import importlib
import pkgutil

import migration.validators


def load_validators():
    validators = []

    for module_info in pkgutil.iter_modules(
        migration.validators.__path__
    ):
        module_name = module_info.name

        if module_name in {
            "__init__",
            "loader",
        }:
            continue

        module = importlib.import_module(
            f"migration.validators.{module_name}"
        )

        validate = getattr(
            module,
            "validate",
            None,
        )

        if callable(validate):
            validators.append(validate)

    return validators
