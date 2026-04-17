"""Interview-Agent: Leitfaden + Transkript."""
from __future__ import annotations
import time
from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import (
    SubagentResult, claude_opus_complete, render_prompt,
    emit_start, emit_done,
)
from scripts.media.pdf_render import render_markdown_to_pdf
from scripts.utils import log

PHASE = 4
NAME = "interview"

SYSTEM = "Du erstellst realistische Interview-Inhalte. Keine Meta-Kommentare."

async def run(u: Universe) -> tuple[SubagentResult, str]:
    """Returns (result, transkript_markdown) — Audio-Agent braucht das Transkript."""
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    leitfaden_md = await claude_opus_complete(
        system=SYSTEM,
        user=render_prompt("interview_leitfaden.j2", u=u),
        max_tokens=2048,
    )
    transkript_md = await claude_opus_complete(
        system=SYSTEM,
        user=render_prompt("interview_transkript.j2", u=u, leitfaden=leitfaden_md),
        max_tokens=6000,
        stream=True, phase=PHASE, task_name=NAME,
    )

    leit_pdf = config.ARTIFACTS_DIR / "12a_interview_leitfaden.pdf"
    trans_pdf = config.ARTIFACTS_DIR / "12_interview_transkript.pdf"
    render_markdown_to_pdf(leitfaden_md, leit_pdf, template_name="konzept_html.j2", extra_ctx={"u": u})
    render_markdown_to_pdf(transkript_md, trans_pdf, template_name="konzept_html.j2", extra_ctx={"u": u})
    (config.ARTIFACTS_DIR / "12_interview_transkript.md").write_text(transkript_md, encoding="utf-8")

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"{trans_pdf.name}")
    log.info(f"[{NAME}] Transkript fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=trans_pdf, duration_s=duration), transkript_md
