from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class MigrationConfig:
    source: Path
    output: Path
    reports: Path

    project: Path | None = None
    redirects_file: Path | None = None

    allowed_domains: list[str] = field(
        default_factory=list
    )

    framework_command: list[str] = field(
        default_factory=list
    )

    media_extensions: tuple[str, ...] = (
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".gif",
        ".svg",
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
    )

    html_extensions: tuple[str, ...] = (
        ".html",
        ".htm",
    )

    def prepare_directories(self) -> None:
        self.output.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.reports.mkdir(
            parents=True,
            exist_ok=True,
        )
