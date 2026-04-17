"""Audio-Agent: Transkript → MP3 mit zwei Stimmen."""
from __future__ import annotations
import re
import time
from pathlib import Path
from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import SubagentResult, emit_start, emit_done, emit_warn
from scripts.media.tts_elevenlabs import synth_turn, concat_mp3s
from scripts.utils import log

PHASE = 4
NAME = "audio"

# Regex: **Luca:** oder **Dr. Weber:** am Zeilenanfang
_SPEAKER_RE = re.compile(r"^\*\*(Luca|Dr\. Weber|Dr\.\s?Andrea Weber)[:]\*\*\s*(.*)$", re.MULTILINE)


def parse_turns(transkript_md: str) -> list[tuple[str, str]]:
    """Returns list of (speaker, text)."""
    turns: list[tuple[str, str]] = []
    for m in _SPEAKER_RE.finditer(transkript_md):
        speaker = "luca" if m.group(1).lower().startswith("luca") else "weber"
        text = m.group(2).strip()
        # Strip marker wie [kurze Pause] etc.
        text = re.sub(r"\[[^\]]+\]", "", text).strip()
        if text:
            turns.append((speaker, text))
    return turns


async def run(u: Universe, transkript_md: str) -> SubagentResult:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()
    turns = parse_turns(transkript_md)
    if not turns:
        await emit_warn(NAME, PHASE, "Keine Turns im Transkript gefunden!")
        return SubagentResult(name=NAME, output_path=None, duration_s=0)

    tmp_dir = config.OUTPUT_DIR / "audio_tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    parts: list[Path] = []
    voice_luca = u.schuelerin.voice_id_elevenlabs
    voice_weber = u.interviewperson.tts_voice_id

    # Budget: max 60 Turns, 8 Min Audio. Bei mehr: kürzen.
    for i, (spk, text) in enumerate(turns[:60]):
        vid = voice_luca if spk == "luca" else voice_weber
        part = tmp_dir / f"t{i:03d}_{spk}.mp3"
        synth_turn(vid, text, part)
        parts.append(part)

    out = config.ARTIFACTS_DIR / "13_interview_audio.mp3"
    concat_mp3s(parts, out, pause_ms=400)
    # Cleanup tmp
    for p in parts:
        p.unlink(missing_ok=True)

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"{out.stat().st_size // 1024} KB")
    log.info(f"[{NAME}] Audio fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=out, duration_s=duration)
