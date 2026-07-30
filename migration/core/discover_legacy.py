import csv
import posixpath
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup


PROYECTO = Path("/opt/homeserver/apps/clubrugbyferrol")
ORIGEN = Path(
    "/opt/homeserver/migration/clubrugbyferrol/"
    "clubrugbyferrol.com"
)
SALIDA = PROYECTO / "artifacts/auditoria"
INFORME = PROYECTO / "docs/AUDITORIA_MIGRACION.md"

SALIDA.mkdir(parents=True, exist_ok=True)


def normalizar_ruta(valor: str) -> str | None:
    if not valor:
        return None

    valor = valor.strip()

    if valor.startswith(
        ("#", "mailto:", "tel:", "javascript:")
    ):
        return None

    parsed = urlparse(valor)

    if (
        parsed.netloc
        and "clubrugbyferrol.com" not in parsed.netloc
    ):
        return None

    ruta = parsed.path or "/"

    if not ruta.startswith("/"):
        ruta = "/" + ruta

    ruta = posixpath.normpath(ruta)

    if ruta.endswith(".html"):
        ruta = ruta[:-5]

    if ruta in ("/index", "/index/"):
        ruta = "/"

    return ruta

def auditar_html():


    paginas = []
    enlaces = []
    recursos = []

    for archivo in sorted(ORIGEN.rglob("*.html")):
        relativo = archivo.relative_to(ORIGEN)

        html = archivo.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        titulo = ""

        if soup.title:
            titulo = soup.title.get_text(
                " ",
                strip=True,
            )

        texto = soup.get_text(
            " ",
            strip=True,
        )

        es_404 = (
            "404" in texto
            or "¡No la encuentro!" in texto
            or "PÁGINA NO ENCONTRADA" in texto.upper()
        )

        paginas.append({
            "archivo": str(relativo),
            "ruta_inferida": normalizar_ruta(
                "/" + str(relativo)
            ),
            "titulo": titulo,
            "bytes": archivo.stat().st_size,
            "vacio": archivo.stat().st_size == 0,
            "parece_404": es_404,
        })

        for nodo in soup.select("a[href]"):
            href = nodo.get("href", "")

            enlaces.append({
                "archivo_origen": str(relativo),
                "href": href,
                "ruta_normalizada": normalizar_ruta(
                    href
                ),
                "texto": nodo.get_text(
                    " ",
                    strip=True,
                ),
            })

        for selector, atributo, tipo in (
            ("img[src]", "src", "imagen"),
            ("script[src]", "src", "script"),
            ("link[href]", "href", "recurso"),
            ("iframe[src]", "src", "iframe"),
            ("form[action]", "action", "formulario"),
        ):
            for nodo in soup.select(selector):
                recursos.append({
                    "archivo_origen": str(relativo),
                    "tipo": tipo,
                    "valor": nodo.get(
                        atributo,
                        "",
                    ),
                })

    return paginas, enlaces, recursos


def inventariar_archivos():
    extensiones = {
        ".jpg", ".jpeg", ".png", ".webp",
        ".gif", ".svg", ".pdf",
        ".doc", ".docx", ".xls", ".xlsx",
    }

    archivos = []

    for archivo in sorted(ORIGEN.rglob("*")):
        if not archivo.is_file():
            continue

        if archivo.suffix.lower() not in extensiones:
            continue

        archivos.append({
            "archivo": str(
                archivo.relative_to(ORIGEN)
            ),
            "extension": archivo.suffix.lower(),
            "bytes": archivo.stat().st_size,
        })

    return archivos


def cargar_json(nombre: str, defecto):
    ruta = PROYECTO / "content" / nombre

    if not ruta.exists():
        return defecto

    return json.loads(
        ruta.read_text(encoding="utf-8")
    )


def obtener_rutas_flask():
    comando = [
        "docker",
        "exec",
        "-i",
        "web-clubrugbyferrol",
        "python",
        "-c",
        (
            "from wsgi import app; "
            "[print(r.rule) for r in "
            "sorted(app.url_map.iter_rules(), "
            "key=lambda x: x.rule)]"
        ),
    ]

    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True,
        check=False,
    )

    if resultado.returncode != 0:
        return [], resultado.stderr.strip()

    rutas = [
        linea.strip()
        for linea in resultado.stdout.splitlines()
        if linea.strip()
    ]

    return rutas, ""




def escribir_csv(nombre, filas):
    ruta = SALIDA / nombre

    if not filas:
        ruta.write_text("", encoding="utf-8")
        return

    with ruta.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        escritor = csv.DictWriter(
            f,
            fieldnames=filas[0].keys(),
        )
        escritor.writeheader()
        escritor.writerows(filas)


def generar_informe():

    paginas, enlaces, recursos = auditar_html()
    archivos = inventariar_archivos()
    rutas_flask, error = obtener_rutas_flask()

    escribir_csv(
        "paginas.csv",
        paginas,
    )

    escribir_csv(
        "enlaces.csv",
        enlaces,
    )

    escribir_csv(
        "recursos.csv",
        recursos,
    )

    escribir_csv(
        "archivos.csv",
        archivos,
    )

    redirecciones = cargar_json(
        "redirecciones.json",
        [],
    )

    mapa_redirecciones = {
        item.get("origen"): item.get("destino")
        for item in redirecciones
        if item.get("origen")
    }

    rutas_antiguas = sorted({
        enlace["ruta_normalizada"]
        for enlace in enlaces
        if enlace["ruta_normalizada"]
    })

    rutas_flask_set = set(rutas_flask)

    comparacion = []

    for ruta in rutas_antiguas:
        estado = "PENDIENTE"
        destino = ""

        if ruta in rutas_flask_set:
            estado = "RUTA DIRECTA"
            destino = ruta

        elif ruta in mapa_redirecciones:
            estado = "REDIRECCIÓN"
            destino = mapa_redirecciones[ruta]

        comparacion.append({
            "ruta_antigua": ruta,
            "estado": estado,
            "destino": destino,
        })

    escribir_csv(
        "comparacion_rutas.csv",
        comparacion,
    )

    pendientes = [
        r
        for r in comparacion
        if r["estado"] == "PENDIENTE"
    ]

    informe = [
        "# Auditoría de migración",
        "",
        "## Resumen",
        "",
        f"- HTML analizados: {len(paginas)}",
        f"- Enlaces encontrados: {len(enlaces)}",
        f"- Recursos encontrados: {len(recursos)}",
        f"- Archivos multimedia: {len(archivos)}",
        f"- Rutas Flask: {len(rutas_flask)}",
        f"- Redirecciones: {len(mapa_redirecciones)}",
        f"- URLs antiguas: {len(rutas_antiguas)}",
        f"- Pendientes: {len(pendientes)}",
        "",
        "## Pendientes",
        "",
    ]

    if pendientes:
        for item in pendientes:
            informe.append(
                f"- {item['ruta_antigua']}"
            )
    else:
        informe.append("- Ninguna")

    informe.append("")
    informe.append("## Rutas Flask")
    informe.append("")

    if error:
        informe.append(error)
    else:
        for ruta in sorted(rutas_flask):
            informe.append(f"- {ruta}")

    (PROYECTO / "docs" / "AUDITORIA_MIGRACION.md").write_text(
        "\n".join(informe) + "\n",
        encoding="utf-8",
    )

    print("Auditoría finalizada.")


if __name__ == "__main__":
    generar_informe()
