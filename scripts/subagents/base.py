"""Gemeinsames Protokoll aller Subagenten."""
from __future__ import annotations
import asyncio
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from anthropic import AsyncAnthropic
from jinja2 import Environment, FileSystemLoader, select_autoescape

from scripts import config
from scripts.event_bus import Event, get_bus
from scripts.coherence import Universe, load_universe
from scripts.utils import log

_jinja = Environment(
    loader=FileSystemLoader(str(config.PROMPTS_DIR)),
    autoescape=select_autoescape(default=False),
    keep_trailing_newline=True,
)

_client: AsyncAnthropic | None = None

def claude() -> AsyncAnthropic:
    global _client
    if _client is None:
        _client = AsyncAnthropic(api_key=config.ANTHROPIC_API_KEY)
    return _client

def render_prompt(template_name: str, **ctx) -> str:
    tpl = _jinja.get_template(template_name)
    return tpl.render(**ctx)

@dataclass
class SubagentResult:
    name: str
    output_path: Path | None
    duration_s: float
    cost_usd: float = 0.0
    meta: dict | None = None

async def emit_start(name: str, phase: int):
    await get_bus().emit(Event(type="subtask", data={"phase": phase, "task": name, "status": "running"}))

async def emit_done(name: str, phase: int, detail: str = ""):
    await get_bus().emit(Event(type="subtask", data={"phase": phase, "task": name, "status": "done", "detail": detail}))

async def emit_warn(name: str, phase: int, message: str):
    await get_bus().emit(Event(type="error", data={"phase": phase, "task": name, "severity": "warn", "message": message}))

async def emit_token(name: str, phase: int, delta: str):
    await get_bus().emit(Event(type="stream", data={"phase": phase, "task": name, "delta": delta}))

async def claude_opus_complete(system: str, user: str, max_tokens: int = 4096, stream: bool = False, phase: int = 0, task_name: str = "") -> str:
    """Claude Opus-Aufruf. Wenn stream=True, werden Tokens per event_bus gestreamt."""
    start = time.monotonic()
    client = claude()
    if stream:
        chunks: list[str] = []
        async with client.messages.stream(
            model=config.CLAUDE_MODEL_OPUS,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        ) as s:
            async for delta in s.text_stream:
                chunks.append(delta)
                if task_name:
                    await emit_token(task_name, phase, delta)
        return "".join(chunks)
    resp = await client.messages.create(
        model=config.CLAUDE_MODEL_OPUS,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return resp.content[0].text if resp.content else ""

async def claude_sonnet_complete(system: str, user: str, max_tokens: int = 4096) -> str:
    client = claude()
    resp = await client.messages.create(
        model=config.CLAUDE_MODEL_SONNET,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return resp.content[0].text if resp.content else ""
