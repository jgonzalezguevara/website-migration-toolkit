from pathlib import Path
from typing import Any, Iterable

from migration.models.inventory import InventoryItem
from migration.models.mapping import MigrationMapItem
from migration.models.validation import ValidationIssue
from migration.reporting.csv import write_csv
from migration.reporting.json import write_json
from migration.reporting.markdown import (
    write_validation_markdown,
)
from migration.reporting.statistics import (
    build_statistics,
)


class ReportManager:
    def __init__(
        self,
        output_directory: Path,
    ) -> None:
        self.output_directory = output_directory
        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def csv(
        self,
        filename: str,
        rows: Iterable[Any],
    ) -> Path:
        destination = (
            self.output_directory / filename
        )

        write_csv(
            destination,
            rows,
        )

        return destination

    def json(
        self,
        filename: str,
        data: Any,
    ) -> Path:
        destination = (
            self.output_directory / filename
        )

        write_json(
            destination,
            data,
        )

        return destination

    def inventory(
        self,
        items: Iterable[InventoryItem],
        filename: str = "inventory.csv",
    ) -> Path:
        return self.csv(
            filename,
            items,
        )

    def validation(
        self,
        issues: Iterable[ValidationIssue],
        csv_filename: str = "validation.csv",
        markdown_filename: str = "validation.md",
    ) -> tuple[Path, Path]:
        issue_items = list(issues)

        csv_path = self.csv(
            csv_filename,
            issue_items,
        )

        markdown_path = (
            self.output_directory
            / markdown_filename
        )

        write_validation_markdown(
            markdown_path,
            issue_items,
        )

        return csv_path, markdown_path

    def migration_map(
        self,
        items: Iterable[MigrationMapItem],
        filename: str = "migration-map.csv",
    ) -> Path:
        return self.csv(
            filename,
            items,
        )

    def statistics(
        self,
        inventory: Iterable[InventoryItem],
        issues: Iterable[ValidationIssue],
        filename: str = "statistics.json",
    ) -> dict:
        data = build_statistics(
            inventory,
            issues,
        )

        self.json(
            filename,
            data,
        )

        return data
