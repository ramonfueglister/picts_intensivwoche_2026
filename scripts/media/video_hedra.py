"""Hedra Character-2: Lip-Sync aus Foto + Audio."""
from __future__ import annotations
import asyncio
import time
from pathlib import Path
import httpx

from scripts import config

BASE = "https://api.hedra.com/web-app/public"
HEADERS = {"X-API-Key": config.HEDRA_API_KEY}

async def generate_lipsync(image_path: Path, audio_path: Path, out: Path, duration_s: int = 20) -> Path:
    async with httpx.AsyncClient(timeout=60) as client:
        # 1. Upload Bild
        with image_path.open("rb") as f:
            img_up = await client.post(f"{BASE}/assets", headers=HEADERS, files={"file": (image_path.name, f, "image/png")})
        img_up.raise_for_status()
        img_id = img_up.json()["id"]
        # 2. Upload Audio (trimmen auf duration_s via ffmpeg vorher)
        trimmed = audio_path.parent / "_hedra_trim.mp3"
        import subprocess
        subprocess.run(["ffmpeg", "-y", "-i", str(audio_path), "-t", str(duration_s), "-c", "copy", str(trimmed)], check=True, capture_output=True)
        with trimmed.open("rb") as f:
            aud_up = await client.post(f"{BASE}/assets", headers=HEADERS, files={"file": (trimmed.name, f, "audio/mpeg")})
        aud_up.raise_for_status()
        aud_id = aud_up.json()["id"]
        trimmed.unlink(missing_ok=True)
        # 3. Generation starten
        gen = await client.post(f"{BASE}/generations", headers=HEADERS, json={
            "type": "character-2", "image_id": img_id, "audio_id": aud_id, "resolution": "720p",
        })
        gen.raise_for_status()
        gen_id = gen.json()["id"]
        # 4. Poll
        for _ in range(60):
            await asyncio.sleep(5)
            s = await client.get(f"{BASE}/generations/{gen_id}", headers=HEADERS)
            s.raise_for_status()
            d = s.json()
            if d.get("status") == "complete":
                v = await client.get(d["video_url"], timeout=60)
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(v.content)
                return out
            if d.get("status") == "failed":
                raise RuntimeError(f"Hedra failed: {d}")
        raise TimeoutError("Hedra polling timeout")
