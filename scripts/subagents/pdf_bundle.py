"""Finale PDF-Render + ZIP-Bundle. Kein LLM."""
from __future__ import annotations
import time
import zipfile
from pathlib import Path

from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import SubagentResult, emit_start, emit_done
from scripts.media.pdf_render import render_va_final
from scripts.utils import log

PHASE = 8
NAME = "pdf_bundle"

async def run(u: Universe, haupttext_md: str) -> SubagentResult:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    main_pdf = config.ARTIFACTS_DIR / "03_va_hauptarbeit.pdf"
    anon_pdf = config.ARTIFACTS_DIR / "04_va_hauptarbeit_anonym.pdf"
    geb_pdf = config.ARTIFACTS_DIR / "05_va_hauptarbeit_gebunden.pdf"
    render_va_final(haupttext_md, u, main_pdf, anon_pdf, geb_pdf)

    # ZIP-Bundle
    zip_path = config.OUTPUT_DIR / "va_komplett.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(config.ARTIFACTS_DIR.rglob("*")):
            if p.is_file():
                zf.write(p, arcname=p.relative_to(config.ARTIFACTS_DIR))

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"ZIP {zip_path.stat().st_size // 1024} KB")
    log.info(f"[{NAME}] Bundle fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=zip_path, duration_s=duration)
