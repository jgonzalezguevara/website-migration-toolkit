from collections.abc import Iterator
from pathlib import Path


def find_files(
    root: Path,
    extensions: tuple[str, ...] | None = None,
) -> Iterator[Path]:

    for file in sorted(root.rglob("*")):

        if not file.is_file():
            continue

        if (
            extensions is not None
            and file.suffix.lower() not in extensions
        ):
            continue

        yield file
