# Website Migration Toolkit

Website Migration Toolkit es una herramienta diseñada para automatizar la migración de sitios web heredados hacia plataformas modernas.

El proyecto permite descubrir el contenido de una web, generar un inventario completo, importar contenido estructurado y validar que la migración se ha realizado correctamente.

## Flujo de trabajo

```
Legacy Website
       │
       ▼
   Discover
       │
       ▼
   Inventory
       │
       ▼
    Import
       │
       ▼
   Validate
       │
       ▼
 Coverage Report
```

## Características

- Descubrimiento automático de páginas y recursos.
- Inventario de contenido.
- Detección de enlaces internos.
- Validación automática de la migración.
- Generación de informes Markdown y CSV.
- Cobertura real de la migración.

## Estado

Proyecto en desarrollo.

## Validation

Version 0.3.0 introduces the first validation pipeline.

The validation engine currently:

- checks internal links against discovered routes;
- resolves relative links from their source HTML file;
- ignores external URLs and unsupported protocols;
- deduplicates repeated issues by source file and normalized target;
- returns structured `ValidationIssue` objects;
- supports registering additional validators through the validation orchestrator.

Current commands:

```bash
python3 -m migration.main discover \
  --source /path/to/site \
  --output /path/to/output

python3 -m migration.main inventory \
  --source /path/to/site \
  --output /path/to/output
```

> The `validate` command will be exposed through the CLI in the next iteration.
