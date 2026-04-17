"""Self-Check-Agent: Rubrik-Bewertung der finalen Artefakte."""
from __future__ import annotations
import json
import time
from scripts import config
from scripts.coherence import Universe
from scripts.rubric_parser import load_rubric
from scripts.subagents.base import (
    SubagentResult, claude_opus_complete, render_prompt,
    emit_start, emit_done,
)
from scripts.event_bus import Event, get_bus
from scripts.utils import atomic_write_json, log

PHASE = 7
NAME = "self_check"
SYSTEM = "Du bist Prüfexpert:in für VA-Bewertung. Du antwortest nur mit gültigem JSON."


def _read_excerpt(path, n=4000) -> str:
    from pathlib import Path
    p = Path(path)
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8")[:n]


async def run(u: Universe) -> tuple[SubagentResult, dict]:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    rubric = load_rubric()
    artifacts = [p.name for p in config.ARTIFACTS_DIR.iterdir() if p.is_file()]

    user = render_prompt("self_check.j2",
        rubric_json=json.dumps(rubric.model_dump(), ensure_ascii=False),
        artifacts=sorted(artifacts),
        haupttext_excerpt=_read_excerpt(config.ARTIFACTS_DIR / "03_va_hauptarbeit.md", 6000),
        konzept_excerpt=_read_excerpt(config.ARTIFACTS_DIR / "02_konzept.md", 3000),
        journal_excerpt=_read_excerpt(config.ARTIFACTS_DIR / "06_projektjournal.md", 3000),
        reflexion_excerpt=_read_excerpt(config.ARTIFACTS_DIR / "09_gesamtreflexion.md", 3000),
    )
    raw = await claude_opus_complete(system=SYSTEM, user=user, max_tokens=3500)
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
    report = json.loads(raw)

    atomic_write_json(config.OUTPUT_DIR / "score_report.json", report)
    await get_bus().emit(Event(type="score", data={"total": report["total"], "note": report["note"], "breakdown": report["teile"]}))

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"{report['total']}/120 Pkt = Note {report['note']}")
    log.info(f"[{NAME}] Score {report['total']}/120 in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=None, duration_s=duration), report
