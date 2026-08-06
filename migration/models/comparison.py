from dataclasses import dataclass


@dataclass(slots=True)
class ComparisonItem:
    path: str
    status: str
    old_extension: str = ""
    new_extension: str = ""
    old_category: str = ""
    new_category: str = ""
    old_size: int = 0
    new_size: int = 0
    size_difference: int = 0
    old_sha256: str = ""
    new_sha256: str = ""
