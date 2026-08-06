from dataclasses import asdict, dataclass


@dataclass(slots=True)
class MigrationMapItem:
    source_file: str
    old_route: str
    new_route: str = ""
    status: str = "pending"
    action: str = "review"

    def to_dict(self) -> dict:
        return asdict(self)
