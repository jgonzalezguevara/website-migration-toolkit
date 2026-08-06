from pathlib import Path

from migration.core.redirects import load_redirects
from migration.models.mapping import MigrationMapItem
from migration.reporting.csv import write_csv


def build_migration_map(
    pages,
    output: Path | None = None,
    redirects_file: Path | None = None,
):
    items = []
    redirects = load_redirects(
        redirects_file
    )

    for page in pages:
        old_route = page.inferred_route or ""

        status = "pending"
        action = "review"
        new_route = ""

        if page.empty:
            status = "ignore"
            action = "ignore-empty-page"

        elif page.appears_404:
            status = "ignore"
            action = "ignore-404-page"

        elif old_route in redirects:
            status = "redirect"
            action = "create-redirect"
            new_route = redirects[old_route]

        elif old_route:
            status = "direct"
            action = "keep-route"
            new_route = old_route

        items.append(
            MigrationMapItem(
                source_file=page.file,
                old_route=old_route,
                new_route=new_route,
                status=status,
                action=action,
            )
        )

    if output is not None:
        write_csv(
            output / "migration-map.csv",
            items,
        )

    return items
