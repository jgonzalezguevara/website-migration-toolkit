from migration.config import MigrationConfig
from migration.parsers.html import parse_html_file
from migration.reporting.csv import write_csv
from migration.utils.filesystem import find_files


def discover(config: MigrationConfig):

    config.prepare_directories()

    pages = []
    links = []
    resources = []

    for html in find_files(
        config.source,
        config.html_extensions,
    ):

        page, page_links, page_resources = parse_html_file(
            html,
            config.source,
            config.allowed_domains,
        )

        pages.append(page)
        links.extend(page_links)
        resources.extend(page_resources)

    write_csv(
        config.output / "pages.csv",
        pages,
    )

    write_csv(
        config.output / "links.csv",
        links,
    )

    write_csv(
        config.output / "resources.csv",
        resources,
    )

    return pages, links, resources
