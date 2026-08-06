import argparse
from pathlib import Path
from urllib.parse import urlparse

from migration.config import MigrationConfig
from migration.core.crawler import crawl_site
from migration.core.discover import discover
from migration.core.inventory import build_inventory
from migration.core.mapping import build_migration_map
from migration.core.validate import run_validation
from migration.reporting.csv import write_csv
from migration.reporting.markdown import write_validation_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="website-migration-toolkit",
        description=(
            "Toolkit para descargar, descubrir, inventariar, "
            "validar y preparar migraciones web."
        ),
    )

    commands = parser.add_subparsers(
        dest="command",
        required=True,
    )

    discover_parser = commands.add_parser(
        "discover",
        help="Analiza páginas HTML, enlaces y recursos.",
    )

    discover_parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Directorio raíz del sitio web.",
    )

    discover_parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Directorio de salida de los CSV.",
    )

    discover_parser.add_argument(
        "--domain",
        action="append",
        default=[],
        help="Dominio permitido. Puede repetirse.",
    )

    inventory_parser = commands.add_parser(
        "inventory",
        help="Genera el inventario de archivos del sitio.",
    )

    inventory_parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Directorio raíz que se va a inventariar.",
    )

    inventory_parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Directorio de salida del inventario.",
    )

    validate_parser = commands.add_parser(
        "validate",
        help="Valida enlaces y genera incidencias.",
    )

    validate_parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Directorio raíz del sitio.",
    )

    validate_parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Directorio de salida.",
    )

    validate_parser.add_argument(
        "--domain",
        action="append",
        default=[],
        help="Dominio permitido.",
    )

    map_parser = commands.add_parser(
        "map",
        help="Genera el mapa inicial de migración.",
    )

    map_parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Directorio raíz del sitio.",
    )

    map_parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Directorio de salida.",
    )

    map_parser.add_argument(
        "--domain",
        action="append",
        default=[],
        help="Dominio permitido.",
    )

    map_parser.add_argument(
        "--redirects",
        type=Path,
        help="CSV con old_route y new_route.",
    )

    migrate_parser = commands.add_parser(
        "migrate",
        help="Descarga y analiza automáticamente un sitio web.",
    )

    migrate_parser.add_argument(
        "url",
        help="URL pública del sitio que se va a migrar.",
    )

    migrate_parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Directorio del proyecto de migración.",
    )

    migrate_parser.add_argument(
        "--redirects",
        type=Path,
        help="CSV opcional con old_route y new_route.",
    )

    return parser


def validate_source(
    parser: argparse.ArgumentParser,
    source: Path,
) -> None:
    if not source.exists():
        parser.error(
            f"El directorio de origen no existe: {source}"
        )

    if not source.is_dir():
        parser.error(
            f"El origen no es un directorio: {source}"
        )


def build_config(
    source: Path,
    output: Path,
    domains: list[str],
) -> MigrationConfig:
    return MigrationConfig(
        source=source,
        output=output,
        reports=output,
        allowed_domains=domains,
    )


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "migrate":
        parsed = urlparse(args.url)

        if parsed.scheme not in {"http", "https"}:
            parser.error(
                "La URL debe comenzar por http:// o https://"
            )

        if not parsed.netloc:
            parser.error(
                "La URL no contiene un dominio válido"
            )

        project_root = args.output
        source_dir = project_root / "source"
        report_dir = project_root / "reports"

        site_root = crawl_site(
            args.url,
            source_dir,
        )

        config = build_config(
            site_root,
            report_dir,
            [parsed.netloc],
        )

        pages, links, resources = discover(config)

        inventory = build_inventory(
            site_root,
            report_dir,
        )

        issues = run_validation(
            pages,
            links,
            resources,
            site_root,
        )

        write_csv(
            report_dir / "validation.csv",
            issues,
        )

        write_validation_markdown(
            report_dir / "validation.md",
            issues,
        )

        mapping = build_migration_map(
            pages,
            report_dir,
            args.redirects,
        )

        print(f"Sitio: {args.url}")
        print(f"Páginas: {len(pages)}")
        print(f"Enlaces: {len(links)}")
        print(f"Recursos: {len(resources)}")
        print(f"Archivos: {len(inventory)}")
        print(f"Incidencias: {len(issues)}")
        print(f"Rutas: {len(mapping)}")
        print(f"Salida: {project_root}")

        return 0

    validate_source(
        parser,
        args.source,
    )

    if args.command == "discover":
        config = build_config(
            args.source,
            args.output,
            args.domain,
        )

        pages, links, resources = discover(config)

        print(f"Páginas: {len(pages)}")
        print(f"Enlaces: {len(links)}")
        print(f"Recursos: {len(resources)}")
        print(f"Salida: {args.output}")

        return 0

    if args.command == "inventory":
        items = build_inventory(
            args.source,
            args.output,
        )

        print(f"Archivos: {len(items)}")
        print(
            f"Salida: "
            f"{args.output / 'inventory.csv'}"
        )

        return 0

    if args.command == "validate":
        config = build_config(
            args.source,
            args.output,
            args.domain,
        )

        pages, links, resources = discover(config)

        issues = run_validation(
            pages,
            links,
            resources,
            config.source,
        )

        write_csv(
            args.output / "validation.csv",
            issues,
        )

        write_validation_markdown(
            args.output / "validation.md",
            issues,
        )

        print(f"Páginas: {len(pages)}")
        print(f"Enlaces: {len(links)}")
        print(f"Recursos: {len(resources)}")
        print(f"Incidencias: {len(issues)}")

        return 0

    if args.command == "map":
        config = build_config(
            args.source,
            args.output,
            args.domain,
        )

        pages, _, _ = discover(config)

        items = build_migration_map(
            pages,
            args.output,
            args.redirects,
        )

        print(f"Rutas: {len(items)}")
        print(
            f"Salida: "
            f"{args.output / 'migration-map.csv'}"
        )

        return 0

    parser.error(
        f"Comando no soportado: {args.command}"
    )

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
