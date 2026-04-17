"""Konzept-Subagent. Pattern-Setter für alle anderen LLM-Subagenten."""
from __future__ import annotations
import time
from pathlib import Path

from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import (
    SubagentResult, claude_opus_complete, render_prompt,
    emit_start, emit_done, emit_warn,
)
from scripts.media.pdf_render import render_markdown_to_pdf
from scripts.utils import log

PHASE = 3
NAME = "konzept"

SYSTEM = "Du schreibst Texte für eine Schweizer FaGe-Vertiefungsarbeit. Du schreibst in der ICH-Form aus Sicht der Lernenden. Kein Meta-Kommentar, kein 'ich würde schreiben'."

async def run(u: Universe) -> SubagentResult:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()
    user_prompt = render_prompt("konzept.j2", u=u)
    markdown = await claude_opus_complete(system=SYSTEM, user=user_prompt, max_tokens=4096, stream=True, phase=PHASE, task_name=NAME)
    out = config.ARTIFACTS_DIR / "02_konzept.pdf"
    render_markdown_to_pdf(markdown, out, template_name="konzept_html.j2", extra_ctx={"u": u})
    # auch markdown als Quelle speichern (für Self-Check)
    (config.ARTIFACTS_DIR / "02_konzept.md").write_text(markdown, encoding="utf-8")
    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"{out.name} ({out.stat().st_size // 1024} KB)")
    log.info(f"[{NAME}] Konzept fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=out, duration_s=duration)
