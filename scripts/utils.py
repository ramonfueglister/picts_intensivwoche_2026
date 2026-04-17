"""Gemeinsame Utilities: logger, retry, atomic-write."""
from __future__ import annotations
import asyncio
import json
import logging
import tempfile
from pathlib import Path
from typing import Any, Callable, TypeVar

from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger("va-agent")

T = TypeVar("T")

async def retry_async(fn: Callable[[], Any], attempts: int = 3, base_delay: float = 1.0, name: str = "op"):
    last_exc: Exception | None = None
    for i in range(attempts):
        try:
            return await fn()
        except Exception as e:
            last_exc = e
            log.warning(f"{name} attempt {i+1}/{attempts} failed: {e}")
            if i < attempts - 1:
                await asyncio.sleep(base_delay * (2 ** i))
    assert last_exc is not None
    raise last_exc

def atomic_write_json(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=path.parent) as tf:
        json.dump(data, tf, ensure_ascii=False, indent=2)
        tmp = Path(tf.name)
    tmp.replace(path)

def atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("wb", delete=False, dir=path.parent) as tf:
        tf.write(data)
        tmp = Path(tf.name)
    tmp.replace(path)
