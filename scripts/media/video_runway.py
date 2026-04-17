"""Runway Gen-4 Turbo: 5-8-Sek B-Roll."""
from __future__ import annotations
import asyncio
import time
from pathlib import Path
import httpx

from scripts import config

BASE = "https://api.dev.runwayml.com/v1"
HEADERS = {"Authorization": f"Bearer {config.RUNWAYML_API_KEY}", "X-Runway-Version": "2024-11-06"}

async def generate_broll(prompt: str, out: Path, duration_s: int = 6) -> Path:
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{BASE}/text_to_video", json={
            "promptText": prompt,
            "model": "gen4_turbo",
            "duration": duration_s,
            "ratio": "1280:768",
        }, headers=HEADERS)
        r.raise_for_status()
        task_id = r.json()["id"]
        # Poll
        for _ in range(60):  # max 5 Min
            await asyncio.sleep(5)
            s = await client.get(f"{BASE}/tasks/{task_id}", headers=HEADERS)
            s.raise_for_status()
            status = s.json()
            if status["status"] == "SUCCEEDED":
                video_url = status["output"][0]
                v = await client.get(video_url, timeout=60)
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(v.content)
                return out
            if status["status"] == "FAILED":
                raise RuntimeError(f"Runway failed: {status}")
        raise TimeoutError("Runway polling timeout")
