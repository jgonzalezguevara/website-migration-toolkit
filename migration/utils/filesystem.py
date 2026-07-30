from pathlib import Path


def find_files(
    root: Path,
    extensions: tuple[str, ...],
):

    for file in sorted(root.rglob("*")):

        if not file.is_file():
            continue

        if file.suffix.lower() not in extensions:
            continue

        yield file
