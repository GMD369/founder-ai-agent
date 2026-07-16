import re
from datetime import datetime

from smolagents import tool

from config import REPORTS_DIR


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:60] or "startup-idea"


@tool
def save_report(startup_name: str, markdown_content: str) -> str:
    """Saves the final investor-style validation report to disk as a Markdown file.

    Args:
        startup_name: Short name or slug of the startup idea, used to name the file.
        markdown_content: The full report content, formatted in Markdown.

    Returns:
        The absolute file path where the report was saved.
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{_slugify(startup_name)}-{timestamp}.md"
    path = REPORTS_DIR / filename
    path.write_text(markdown_content, encoding="utf-8")
    return str(path)
