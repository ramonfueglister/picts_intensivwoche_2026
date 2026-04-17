"""Video-Subagent: B-Roll (Runway) + Lip-Sync (Hedra), parallel."""
from __future__ import annotations
import asyncio
import time
from pathlib import Path
from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import SubagentResult, emit_start, emit_done, emit_warn
from scripts.media.video_runway import generate_broll
from scripts.media.video_hedra import generate_lipsync
from scripts.utils import log

PHASE = 4
NAME = "video"

async def run(u: Universe, weber_image: Path, interview_audio: Path) -> SubagentResult:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    broll_out = config.ARTIFACTS_DIR / "17_video_broll.mp4"
    lipsync_out = config.ARTIFACTS_DIR / "14_interview_video_lipsync.mp4"

    broll_prompt = f"Warme Spitex-Szene, Pflegefachperson besucht ältere alleinlebende Frau zuhause, Tageslicht durchs Fenster, cinematic dokumentarisch, ruhige Kamerafahrt, 35mm Film look."
    results = await asyncio.gather(
        _safe(generate_broll, NAME, "broll", broll_prompt, broll_out, 6),
        _safe(generate_lipsync, NAME, "lipsync", weber_image, interview_audio, lipsync_out, 20),
        return_exceptions=False,
    )
    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"broll={results[0] is not None}, lipsync={results[1] is not None}")
    log.info(f"[{NAME}] Video fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=lipsync_out, duration_s=duration)

async def _safe(fn, parent_name, subname, *args):
    try:
        return await fn(*args)
    except Exception as e:
        await emit_warn(parent_name, PHASE, f"{subname} failed: {e}")
        return None
