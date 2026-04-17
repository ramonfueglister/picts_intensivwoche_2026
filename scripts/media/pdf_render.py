"""HTML/Markdown → PDF via WeasyPrint."""
from __future__ import annotations
from pathlib import Path
import markdown as md_lib
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML, CSS

from scripts import config

_jinja = Environment(
    loader=FileSystemLoader(str(config.TEMPLATES_DIR)),
    autoescape=select_autoescape(["html"]),
)

def load_css() -> str:
    return (config.TEMPLATES_DIR / "va_css.css").read_text(encoding="utf-8")

def render_markdown_to_pdf(markdown: str, out_path: Path, template_name: str = "konzept_html.j2", extra_ctx: dict | None = None) -> None:
    body_html = md_lib.markdown(markdown, extensions=["tables", "fenced_code", "toc"])
    tpl = _jinja.get_template(template_name)
    html_str = tpl.render(
        body_html=body_html,
        css=load_css(),
        **(extra_ctx or {}),
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html_str, base_url=str(config.PROJECT_ROOT)).write_pdf(str(out_path))

def render_html_to_pdf(html_str: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html_str, base_url=str(config.PROJECT_ROOT)).write_pdf(str(out_path))
