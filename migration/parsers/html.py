from pathlib import Path

from bs4 import BeautifulSoup

from migration.models.discovery import (
    Link,
    Page,
    Resource,
)
from migration.utils.routes import normalize_route


def parse_html_file(
    file: Path,
    source_root: Path,
    allowed_domains: list[str],
) -> tuple[Page, list[Link], list[Resource]]:

    relative = file.relative_to(source_root)

    html = file.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    title = ""

    if soup.title:
        title = soup.title.get_text(
            " ",
            strip=True,
        )

    text = soup.get_text(
        " ",
        strip=True,
    )

    appears_404 = (
        "404" in text
        or "PÁGINA NO ENCONTRADA" in text.upper()
        or "PAGE NOT FOUND" in text.upper()
    )

    page = Page(
        file=str(relative),
        inferred_route=normalize_route(
            "/" + str(relative),
            allowed_domains,
        ),
        title=title,
        size=file.stat().st_size,
        empty=file.stat().st_size == 0,
        appears_404=appears_404,
    )

    links = []

    for node in soup.select("a[href]"):
        href = node.get("href", "")

        links.append(
            Link(
                source_file=str(relative),
                href=href,
                normalized_route=normalize_route(
                    href,
                    allowed_domains,
                    str(relative),
                ),
                text=node.get_text(
                    " ",
                    strip=True,
                ),
            )
        )

    resources = []

    selectors = (
        ("img[src]", "src", "image"),
        ("script[src]", "src", "script"),
        ("link[href]", "href", "resource"),
        ("iframe[src]", "src", "iframe"),
        ("form[action]", "action", "form"),
    )

    for selector, attribute, resource_type in selectors:
        for node in soup.select(selector):
            resources.append(
                Resource(
                    source_file=str(relative),
                    type=resource_type,
                    value=node.get(
                        attribute,
                        "",
                    ),
                )
            )

    return page, links, resources
