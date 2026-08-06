from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin
from xml.etree.ElementTree import (
    Element,
    ElementTree,
    SubElement,
    indent,
)

from migration.models.discovery import Page


SITEMAP_NAMESPACE = (
    "http://www.sitemaps.org/schemas/sitemap/0.9"
)


def build_sitemap_urls(
    pages: Iterable[Page],
    base_url: str,
) -> list[str]:
    normalized_base_url = (
        base_url.rstrip("/") + "/"
    )

    urls = set()

    for page in pages:
        route = page.inferred_route

        if not route:
            continue

        if page.empty or page.appears_404:
            continue

        robots = page.robots.lower()

        if "noindex" in robots:
            continue

        absolute_url = urljoin(
            normalized_base_url,
            route.lstrip("/"),
        )

        if route == "/":
            absolute_url = normalized_base_url.rstrip("/")

        urls.add(absolute_url)

    return sorted(urls)


def write_sitemap(
    destination: Path,
    pages: Iterable[Page],
    base_url: str,
) -> Path:
    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    root = Element(
        "urlset",
        {
            "xmlns": SITEMAP_NAMESPACE,
        },
    )

    for url in build_sitemap_urls(
        pages,
        base_url,
    ):
        url_node = SubElement(
            root,
            "url",
        )

        location_node = SubElement(
            url_node,
            "loc",
        )

        location_node.text = url

    tree = ElementTree(root)

    indent(
        tree,
        space="  ",
    )

    tree.write(
        destination,
        encoding="utf-8",
        xml_declaration=True,
    )

    return destination
