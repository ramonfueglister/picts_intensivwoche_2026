"""Redaktor-Agent: Stilpolitur über Haupttext."""
from __future__ import annotations
import time
from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import (
    SubagentResult, claude_sonnet_complete, render_prompt,
    emit_start, emit_done,
)
from scripts.utils import log

PHASE = 6
NAME = "redaktor"
SYSTEM = "Du redigierst deutsche Texte ohne den Inhalt zu verändern. Gib nur den revidierten Text zurück."

async def run(u: Universe, md: str) -> tuple[SubagentResult, str]:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    redigiert = await claude_sonnet_complete(system=SYSTEM,
        user=render_prompt("redaktor.j2", u=u, md=md),
        max_tokens=16000)
    (config.ARTIFACTS_DIR / "03_va_hauptarbeit.md").write_text(redigiert, encoding="utf-8")

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"{len(redigiert)} Zeichen")
    log.info(f"[{NAME}] Redaktor fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=None, duration_s=duration), redigiert
