"""Formular-Agent: Eigenständigkeit + Einverständnis als PDF."""
from __future__ import annotations
import time
from jinja2 import Environment, FileSystemLoader, select_autoescape
from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import SubagentResult, emit_start, emit_done
from scripts.media.signature_svg import signature_svg
from scripts.media.pdf_render import render_html_to_pdf, load_css
from scripts.utils import log

PHASE = 4
NAME = "formular"

_jinja = Environment(loader=FileSystemLoader(str(config.TEMPLATES_DIR)), autoescape=select_autoescape(["html"]))

async def run(u: Universe) -> SubagentResult:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    sig_luca = signature_svg(f"{u.schuelerin.vorname} {u.schuelerin.nachname}")
    sig_weber = signature_svg(u.interviewperson.name_anzeige)
    css = load_css()

    e_html = _jinja.get_template("eigenstaendigkeit_html.j2").render(u=u, css=css, signature_luca=sig_luca)
    ein_html = _jinja.get_template("einverstaendnis_html.j2").render(u=u, css=css, signature_weber=sig_weber)

    e_pdf = config.ARTIFACTS_DIR / "10_eigenstaendigkeitserklaerung.pdf"
    ein_pdf = config.ARTIFACTS_DIR / "11_einverstaendniserklaerung_interview.pdf"
    render_html_to_pdf(e_html, e_pdf)
    render_html_to_pdf(ein_html, ein_pdf)

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail="2 Formulare")
    log.info(f"[{NAME}] Formulare fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=e_pdf, duration_s=duration)
