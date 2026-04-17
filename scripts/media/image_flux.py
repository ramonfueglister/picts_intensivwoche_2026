"""FLUX 1.2 Pro via fal-client."""
from __future__ import annotations
import fal_client
import httpx
from pathlib import Path
from scripts import config

async def generate_image(prompt: str, out: Path, aspect: str = "portrait_4_3") -> Path:
    result = await fal_client.subscribe_async(
        "fal-ai/flux-pro/v1.1",
        arguments={
            "prompt": prompt,
            "image_size": aspect,
            "num_inference_steps": 28,
            "guidance_scale": 3.5,
            "num_images": 1,
            "enable_safety_checker": True,
        },
    )
    img_url = result["images"][0]["url"]
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.get(img_url)
        r.raise_for_status()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(r.content)
    return out
