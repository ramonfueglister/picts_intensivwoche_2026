"""Reflexions-Agent: 2× Zwischenreflexion + 1× Gesamtreflexion."""
from __future__ import annotations
import asyncio
import time
from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import (
    SubagentResult, claude_sonnet_complete, render_prompt,
    emit_start, emit_done,
)
from scripts.media.pdf_render import render_markdown_to_pdf
from scripts.utils import log

PHASE = 4
NAME = "reflexion"
SYSTEM = "Du schreibst reflektierte Texte aus Sicht von Luca Brunner, FaGe-Lernendem. Selbstkritisch, ehrlich, doppelpunkt-gendernd."

async def run(u: Universe) -> SubagentResult:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    z1_task = claude_sonnet_complete(system=SYSTEM,
        user=render_prompt("zwischenreflexion.j2", u=u, nummer=1, datum="2026-01-15"),
        max_tokens=1200)
    z2_task = claude_sonnet_complete(system=SYSTEM,
        user=render_prompt("zwischenreflexion.j2", u=u, nummer=2, datum="2026-02-28"),
        max_tokens=1200)
    gesamt_task = claude_sonnet_complete(system=SYSTEM,
        user=render_prompt("gesamtreflexion.j2", u=u),
        max_tokens=1800)

    z1_md, z2_md, gesamt_md = await asyncio.gather(z1_task, z2_task, gesamt_task)

    z1_pdf = config.ARTIFACTS_DIR / "07_zwischenreflexion_1.pdf"
    z2_pdf = config.ARTIFACTS_DIR / "08_zwischenreflexion_2.pdf"
    gesamt_pdf = config.ARTIFACTS_DIR / "09_gesamtreflexion.pdf"

    render_markdown_to_pdf(f"# Erste Zwischenreflexion\n\n*Luca Brunner · 15.01.2026*\n\n" + z1_md, z1_pdf, template_name="konzept_html.j2", extra_ctx={"u": u})
    render_markdown_to_pdf(f"# Zweite Zwischenreflexion\n\n*Luca Brunner · 28.02.2026*\n\n" + z2_md, z2_pdf, template_name="konzept_html.j2", extra_ctx={"u": u})
    render_markdown_to_pdf(gesamt_md, gesamt_pdf, template_name="konzept_html.j2", extra_ctx={"u": u})
    # .md-Versionen für docx-Integration speichern
    (config.ARTIFACTS_DIR / "07_zwischenreflexion_1.md").write_text(z1_md, encoding="utf-8")
    (config.ARTIFACTS_DIR / "08_zwischenreflexion_2.md").write_text(z2_md, encoding="utf-8")
    (config.ARTIFACTS_DIR / "09_gesamtreflexion.md").write_text(gesamt_md, encoding="utf-8")

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail="3 Reflexionen")
    log.info(f"[{NAME}] Reflexionen fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=gesamt_pdf, duration_s=duration)
