import posixpath
from urllib.parse import urlparse


def normalize_route(
    value: str,
    allowed_domains: list[str] | None = None,
    source_file: str | None = None,
) -> str | None:

    if not value:
        return None

    value = value.strip()

    if value.startswith(
        (
            "#",
            "mailto:",
            "tel:",
            "javascript:",
        )
    ):
        return None

    parsed = urlparse(value)

    if parsed.netloc and allowed_domains:

        if not any(
            domain in parsed.netloc
            for domain in allowed_domains
        ):
            return None

    route = parsed.path or "/"

    if (
        source_file
        and not parsed.netloc
        and parsed.path
        and not parsed.path.startswith("/")
    ):
        base = posixpath.dirname(
            "/" + source_file
        )
        route = posixpath.join(
            base,
            parsed.path,
        )

    if not route.startswith("/"):
        route = "/" + route

    route = posixpath.normpath(route)

    if route.endswith(".html"):
        route = route[:-5]

    if route in (
        "/index",
        "/index/",
    ):
        route = "/"

    return route
