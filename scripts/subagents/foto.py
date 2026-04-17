"""Foto-Subagent: 5 Bilder (Dr. Weber, Luca+Weber, Spitex-Szene, Einsamkeit-Symbol, Umfrage-Zettel)."""
from __future__ import annotations
import asyncio
import time
from pathlib import Path
from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import SubagentResult, emit_start, emit_done
from scripts.media.image_flux import generate_image
from scripts.utils import log

PHASE = 4
NAME = "foto"

async def run(u: Universe) -> tuple[SubagentResult, dict[str, Path]]:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    targets = {
        "weber_portrait": (u.interviewperson.foto_prompt, "portrait_4_3"),
        "luca_weber": (f"Zwei Personen in einem Büro, Frau ca. 50 mit Brille und graumeliertem Haar, junger Mann ca. 19 Jahre daneben, beide lächeln in die Kamera, natürliches Licht, professionelle Bürostimmung", "landscape_4_3"),
        "spitex_szene": ("Pflegefachperson zu Besuch bei älterer Klientin zuhause, ruhige Wohnzimmer-Atmosphäre, Tageslicht, dokumentarische Warmheit", "landscape_4_3"),
        "einsamkeit_symbol": ("Einzelne ältere Person am Fenster, gedämpftes Tageslicht, kontemplativ, schwarzweiss, poetisch, konzeptuell", "portrait_4_3"),
        "umfrage_zettel": ("Papierfragebogen auf Holztisch, Kugelschreiber daneben, Kaffeetasse im Hintergrund, Top-Down-Shot, realistisch", "square"),
    }
    tasks = [generate_image(p, config.ARTIFACTS_DIR / f"foto_{k}.png", a) for k, (p, a) in targets.items()]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    paths = {}
    for k, r in zip(targets.keys(), results):
        if isinstance(r, Path):
            paths[k] = r

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"{len(paths)}/5 Bilder")
    log.info(f"[{NAME}] Fotos fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=None, duration_s=duration), paths
