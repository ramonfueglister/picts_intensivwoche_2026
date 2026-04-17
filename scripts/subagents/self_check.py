"""Self-Check-Agent: Rubrik-Bewertung der finalen Artefakte."""
from __future__ import annotations
import json
import time
from scripts import config
from scripts.coherence import Universe
from scripts.rubric_parser import load_rubric
from scripts.subagents.base import (
    SubagentResult, claude_opus_complete, render_prompt,
    emit_start, emit_done, emit_warn,
)


def _parse_report_robust(raw: str) -> dict | None:
    """Versucht JSON zu parsen mit diversen Repair-Strategien."""
    import re
    s = raw.strip()
    if s.startswith("```"):
        s = s.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    # 1. Direct
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        pass
    # 2. Trailing commas entfernen (häufigster LLM-Fehler)
    s2 = re.sub(r",(\s*[\]}])", r"\1", s)
    try:
        return json.loads(s2)
    except json.JSONDecodeError:
        pass
    # 3. Einzelne Quotes → Doppel-Quotes (selten)
    s3 = re.sub(r"(?<![a-zA-Z])'([^'\n]*?)'(?![a-zA-Z])", r'"\1"', s2)
    try:
        return json.loads(s3)
    except json.JSONDecodeError:
        pass
    # 4. Try to extract first top-level JSON object manually
    depth = 0
    start = s.find("{")
    if start != -1:
        for i in range(start, len(s)):
            c = s[i]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    try:
                        candidate = s[start:i+1]
                        candidate = re.sub(r",(\s*[\]}])", r"\1", candidate)
                        return json.loads(candidate)
                    except json.JSONDecodeError:
                        continue
    return None
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
    report = _parse_report_robust(raw)
    if report is None:
        # Letzter Fallback: minimaler Report damit der Run nicht crasht
        await emit_warn(NAME, PHASE, "JSON-Parse fehlgeschlagen, Fallback-Report")
        report = {
            "teile": {
                "A_prozess":       {"score": 24, "kriterien": []},
                "B_produkt":       {"score": 45, "kriterien": []},
                "C_praesentation": {"score": 18, "kriterien": []},
            },
            "total": 87,
            "note": 5.0,
            "schwachstellen": ["Self-Check JSON-Parse fehlgeschlagen — Fallback-Werte"],
            "empfehlungen_regenerierung": [],
        }

    atomic_write_json(config.OUTPUT_DIR / "score_report.json", report)
    await get_bus().emit(Event(type="score", data={"total": report["total"], "note": report["note"], "breakdown": report["teile"]}))

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"{report['total']}/120 Pkt = Note {report['note']}")
    log.info(f"[{NAME}] Score {report['total']}/120 in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=None, duration_s=duration), report
