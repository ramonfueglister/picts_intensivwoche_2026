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

import re

def render_va_final(markdown: str, u: "Universe", out_main: Path, out_anonym: Path, out_gebunden: Path) -> None:
    """Rendert 3 VA-Versionen: vollständig / anonymisiert / gebunden (mit Bildern)."""
    import markdown as md_lib

    css = load_css()
    # 1. Hauptversion
    body_html = md_lib.markdown(markdown, extensions=["tables", "fenced_code", "toc"])
    tpl = _jinja.get_template("va_html.j2")
    html_main = tpl.render(body_html=body_html, css=css, u=u)
    out_main.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html_main, base_url=str(config.PROJECT_ROOT)).write_pdf(str(out_main))

    # 2. Anonymisierte Version (Wegleitung S. 19: "ohne Bilder, ohne Namen")
    anon_md = _anonymize(markdown, u)
    anon_html = md_lib.markdown(anon_md, extensions=["tables", "fenced_code", "toc"])
    # "ohne Bilder" — entferne <img>-Tags
    anon_html = re.sub(r"<img[^>]*>", "[Bild entfernt – anonymisierte Version]", anon_html)
    u_anon = u.model_copy(deep=True)
    u_anon.schuelerin.vorname = "***"
    u_anon.schuelerin.nachname = "***"
    html_anon = tpl.render(body_html=anon_html, css=css, u=u_anon)
    HTML(string=html_anon, base_url=str(config.PROJECT_ROOT)).write_pdf(str(out_anonym))

    # 3. Gebundene Version (identisch zu Haupt, nur Label)
    out_gebunden.write_bytes(out_main.read_bytes())


def _anonymize(md: str, u) -> str:
    out = md
    for name in [u.schuelerin.vorname, u.schuelerin.nachname,
                 f"{u.schuelerin.vorname} {u.schuelerin.nachname}",
                 u.interviewperson.name_anzeige,
                 "Dr. Weber", "Dr. phil. Andrea Weber",
                 u.schuelerin.lehrperson,
                 u.schuelerin.lehrbetrieb]:
        out = out.replace(name, "***")
    return out
