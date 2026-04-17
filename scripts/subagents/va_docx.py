"""VA-docx-Subagent: nimmt alle generierten Inhalte und füllt die ZAG-Haupt-Vorlage.

Läuft nach Redaktor (Phase 6) parallel zu/nach Self-Check. Produziert eine .docx, die
visuell wie eine echte FaGe-Schüler-Abgabe aussieht (gleiche Vorlage wie im ZAG-Unterricht).
"""
from __future__ import annotations
import time
from pathlib import Path

from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import SubagentResult, emit_start, emit_done, emit_warn
from scripts.media.docx_fill import fill_va_haupt_docx, docx_to_pdf
from scripts.utils import log

PHASE = 8
NAME = "va_docx"


def _read_file(path: Path, default: str = "") -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return default


async def run(u: Universe, haupttext_md: str) -> SubagentResult:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    # Hole generierte Nebentexte aus artifacts/ (wurden von früheren Subagenten geschrieben)
    konzept_md = _read_file(config.ARTIFACTS_DIR / "02_konzept.md", "*Konzept nicht verfügbar*")
    journal_md = _read_file(config.ARTIFACTS_DIR / "06_projektjournal.md", "")
    # Zwischenreflexionen werden nur als PDF gespeichert — ggf. MD daneben ablegen
    z1_md = _read_file(config.ARTIFACTS_DIR / "07_zwischenreflexion_1.md", "")
    z2_md = _read_file(config.ARTIFACTS_DIR / "08_zwischenreflexion_2.md", "")
    gesamt_md = _read_file(config.ARTIFACTS_DIR / "09_gesamtreflexion.md", "")

    out = config.ARTIFACTS_DIR / "00_VA_HAUPTDOKUMENT.docx"
    try:
        fill_va_haupt_docx(u, haupttext_md, konzept_md, journal_md, z1_md, z2_md, gesamt_md, out)
    except Exception as e:
        await emit_warn(NAME, PHASE, f"docx-Fill fehlgeschlagen: {e}")
        log.exception("docx fill failed")
        raise

    # Optional: PDF via LibreOffice (falls installiert)
    pdf = docx_to_pdf(out)
    detail = f"{out.name}"
    if pdf:
        detail += f" + {pdf.name}"

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=detail)
    log.info(f"[{NAME}] VA-docx fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=out, duration_s=duration)
