import subprocess
from pathlib import Path
from urllib.parse import urlparse


WGET_ACCEPTED_RETURN_CODES = {
    0,
    8,
}


def crawl_site(
    url: str,
    output: Path,
) -> Path:
    parsed = urlparse(url)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError(
            "La URL debe comenzar por http:// o https://"
        )

    if not parsed.netloc:
        raise ValueError(
            "La URL no contiene un dominio válido"
        )

    output.mkdir(
        parents=True,
        exist_ok=True,
    )

    command = [
        "wget",
        "--mirror",
        "--convert-links",
        "--adjust-extension",
        "--page-requisites",
        "--no-parent",
        "--execute",
        "robots=off",
        "--directory-prefix",
        str(output),
        url,
    ]

    result = subprocess.run(
        command,
        text=True,
        check=False,
    )

    site_root = output / parsed.netloc

    if not site_root.exists():
        raise RuntimeError(
            f"No se encontró el sitio descargado: {site_root}"
        )

    if result.returncode not in WGET_ACCEPTED_RETURN_CODES:
        raise RuntimeError(
            f"wget finalizó con código {result.returncode}"
        )

    return site_root
