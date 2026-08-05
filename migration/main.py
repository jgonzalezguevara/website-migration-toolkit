import argparse
from pathlib import Path

from migration.config import MigrationConfig
from migration.core.discover import discover
from migration.core.inventory import build_inventory
from migration.core.validate import run_validation
from migration.reporting.csv import write_csv
from migration.reporting.markdown import write_validation_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="website-migration-toolkit",
        description="Toolkit para descubrir, inventariar y validar sitios web.",
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

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.source.exists():
        parser.error(
            f"El directorio de origen no existe: {args.source}"
        )

    if not args.source.is_dir():
        parser.error(
            f"El origen no es un directorio: {args.source}"
        )

    if args.command == "discover":
        config = MigrationConfig(
            source=args.source,
            output=args.output,
            reports=args.output,
            allowed_domains=args.domain,
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
        print(f"Salida: {args.output / 'inventory.csv'}")

        return 0

    if args.command == "validate":
        config = MigrationConfig(
            source=args.source,
            output=args.output,
            reports=args.output,
            allowed_domains=args.domain,
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

    parser.error(f"Comando no soportado: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
