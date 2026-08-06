from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass(slots=True)
class CrawlSettings:
    enabled: bool = True
    robots: bool = False


@dataclass(slots=True)
class TargetSettings:
    framework: str = "html"
    base_url: str = ""


@dataclass(slots=True)
class ProjectSettings:
    name: str
    source_url: str
    output: Path
    target: TargetSettings = field(
        default_factory=TargetSettings
    )
    crawl: CrawlSettings = field(
        default_factory=CrawlSettings
    )
    redirects_file: Path | None = None


def load_project_config(
    path: Path,
) -> ProjectSettings:
    if not path.exists():
        raise FileNotFoundError(
            f"No existe el fichero: {path}"
        )

    data = yaml.safe_load(
        path.read_text(encoding="utf-8")
    ) or {}

    project = data.get("project", {})
    source = data.get("source", {})
    target = data.get("target", {})
    crawl = data.get("crawl", {})
    redirects = data.get("redirects", {})

    name = str(
        project.get("name", "")
    ).strip()

    source_url = str(
        source.get("url", "")
    ).strip()

    output_value = str(
        project.get("output", "")
    ).strip()

    if not name:
        raise ValueError(
            "Falta project.name"
        )

    if not source_url:
        raise ValueError(
            "Falta source.url"
        )

    if not output_value:
        output_value = (
            f"./migration-{name.lower().replace(' ', '-')}"
        )

    redirects_value = str(
        redirects.get("file", "")
    ).strip()

    redirects_file = None

    if redirects_value:
        redirects_file = (
            path.parent / redirects_value
        ).resolve()

    return ProjectSettings(
        name=name,
        source_url=source_url,
        output=Path(output_value).expanduser(),
        target=TargetSettings(
            framework=str(
                target.get("framework", "html")
            ).strip(),
            base_url=str(
                target.get("base_url", "")
            ).strip(),
        ),
        crawl=CrawlSettings(
            enabled=bool(
                crawl.get("enabled", True)
            ),
            robots=bool(
                crawl.get("robots", False)
            ),
        ),
        redirects_file=redirects_file,
    )
