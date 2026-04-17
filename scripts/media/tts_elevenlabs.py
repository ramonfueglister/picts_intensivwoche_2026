"""ElevenLabs TTS: Turn-Sequenz zu einer MP3."""
from __future__ import annotations
from pathlib import Path
from typing import Iterable
from elevenlabs.client import ElevenLabs
import subprocess

from scripts import config

_client: ElevenLabs | None = None

def _c() -> ElevenLabs:
    global _client
    if _client is None:
        _client = ElevenLabs(api_key=config.ELEVENLABS_API_KEY)
    return _client

def synth_turn(voice_id: str, text: str, out: Path, model: str = "eleven_multilingual_v2") -> None:
    audio = _c().text_to_speech.convert(
        voice_id=voice_id, model_id=model, text=text,
        output_format="mp3_44100_128",
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as f:
        for chunk in audio:
            f.write(chunk)

def concat_mp3s(parts: list[Path], out: Path, pause_ms: int = 350) -> None:
    """Concat mit ffmpeg + kurze Stille dazwischen."""
    list_file = out.parent / "concat.txt"
    silence_file = out.parent / "_silence.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo",
        "-t", str(pause_ms / 1000), "-q:a", "9", "-acodec", "libmp3lame", str(silence_file),
    ], check=True, capture_output=True)
    with list_file.open("w") as f:
        for i, p in enumerate(parts):
            f.write(f"file '{p.resolve()}'\n")
            if i < len(parts) - 1:
                f.write(f"file '{silence_file.resolve()}'\n")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
        "-c", "copy", str(out),
    ], check=True, capture_output=True)
    list_file.unlink(missing_ok=True)
    silence_file.unlink(missing_ok=True)
