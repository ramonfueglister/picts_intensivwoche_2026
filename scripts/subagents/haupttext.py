"""Haupttext-Subagent: komplette VA in einem grossen Call."""
from __future__ import annotations
import time
from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import (
    SubagentResult, claude_opus_complete, render_prompt,
    emit_start, emit_done,
)
from scripts.utils import log

PHASE = 5
NAME = "haupttext"
SYSTEM = """Du bist Luca Brunner, FaGe-Lernender im 5. Semester. Du schreibst deine Vertiefungsarbeit.
ICH-Form. Doppelpunkt-Gendern. Keine erfundenen Quellen — nutze NUR die explizit aufgeführten.
Keine Meta-Kommentare. Gib nur den Markdown-Haupttext zurück."""


async def run(u: Universe, interview_md: str, umfrage_auswertung_md: str) -> tuple[SubagentResult, str]:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    quellen_short = "\n".join(
        f"- [{q.typ}] {q.autor}: {q.titel} ({q.jahr}) — {q.verlag or q.url or ''}"
        for q in u.quellen
    )
    # Interview-Kernpunkte extrahieren (erste 2000 Zeichen als Summary — für den Prompt-Budget)
    interview_kernpunkte = interview_md[:4000]

    md = await claude_opus_complete(
        system=SYSTEM,
        user=render_prompt("haupttext_kapitel.j2", u=u,
                          quellen_short=quellen_short,
                          umfrage_auswertung=umfrage_auswertung_md[:3000],
                          interview_kernpunkte=interview_kernpunkte),
        max_tokens=16000, stream=True, phase=PHASE, task_name=NAME,
    )
    (config.ARTIFACTS_DIR / "03_va_hauptarbeit.md").write_text(md, encoding="utf-8")

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"{len(md)} Zeichen")
    log.info(f"[{NAME}] Haupttext fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=None, duration_s=duration), md
