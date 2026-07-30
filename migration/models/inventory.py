from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class InventoryItem:
    path: str
    extension: str
    category: str
    size: int
    modified_at: float
    modified_iso: str
    sha256: str | None = None


def classify_file(path: Path) -> str:
    extension = path.suffix.lower()

    categories = {
        "html": {".html", ".htm"},
        "stylesheets": {".css"},
        "javascript": {".js", ".mjs"},
        "images": {
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".svg",
            ".webp",
            ".ico",
        },
        "documents": {
            ".pdf",
            ".doc",
            ".docx",
            ".xls",
            ".xlsx",
            ".ppt",
            ".pptx",
        },
        "audio": {
            ".mp3",
            ".wav",
            ".ogg",
            ".m4a",
        },
        "video": {
            ".mp4",
            ".webm",
            ".avi",
            ".mov",
            ".mkv",
        },
        "fonts": {
            ".woff",
            ".woff2",
            ".ttf",
            ".otf",
            ".eot",
        },
        "data": {
            ".json",
            ".xml",
            ".csv",
            ".yaml",
            ".yml",
        },
    }

    for category, extensions in categories.items():
        if extension in extensions:
            return category

    return "other"
