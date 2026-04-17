"""Journal-Agent: 8 Wocheneinträge."""
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
NAME = "journal"
SYSTEM = "Du schreibst Projektjournal-Einträge aus Sicht von Luca Brunner. ICH-Form. Doppelpunkt-Gendern."

async def run(u: Universe) -> SubagentResult:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    tasks = [
        claude_sonnet_complete(system=SYSTEM, user=render_prompt("journal_woche.j2", u=u, woche=w), max_tokens=1200)
        for w in u.timeline
    ]
    eintraege = await asyncio.gather(*tasks)

    full_md = f"# Projektjournal — {u.schuelerin.vorname} {u.schuelerin.nachname}\n\n"
    full_md += f"**Thema:** {u.thema.titel}\n\n**Lehrperson:** {u.schuelerin.lehrperson}\n\n---\n\n"
    full_md += "\n\n---\n\n".join(eintraege)

    pdf = config.ARTIFACTS_DIR / "06_projektjournal.pdf"
    render_markdown_to_pdf(full_md, pdf, template_name="konzept_html.j2", extra_ctx={"u": u})
    (config.ARTIFACTS_DIR / "06_projektjournal.md").write_text(full_md, encoding="utf-8")

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"{len(eintraege)} Wochen")
    log.info(f"[{NAME}] Journal fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=pdf, duration_s=duration)
