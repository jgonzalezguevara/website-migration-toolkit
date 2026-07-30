from dataclasses import asdict, dataclass


@dataclass(slots=True)
class Page:
    file: str
    inferred_route: str | None
    title: str
    size: int
    empty: bool
    appears_404: bool

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class Link:
    source_file: str
    href: str
    normalized_route: str | None
    text: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class Resource:
    source_file: str
    type: str
    value: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class MediaFile:
    file: str
    extension: str
    size: int

    def to_dict(self) -> dict:
        return asdict(self)
