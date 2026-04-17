"""Pub/Sub-Bus für Subagenten-Events → SSE-Stream."""
from __future__ import annotations
import asyncio
import json
import time
from dataclasses import dataclass, asdict
from typing import Any

@dataclass
class Event:
    type: str
    data: dict[str, Any]
    ts: float = 0.0

    def __post_init__(self):
        if self.ts == 0.0:
            self.ts = time.time()

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

class EventBus:
    def __init__(self, buffer_size: int = 1000):
        self._subscribers: list[asyncio.Queue] = []
        self._history: list[Event] = []
        self._buffer_size = buffer_size

    def subscribe(self, replay_history: bool = True) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue()
        if replay_history:
            for e in self._history:
                q.put_nowait(e)
        self._subscribers.append(q)
        return q

    def unsubscribe(self, q: asyncio.Queue) -> None:
        try:
            self._subscribers.remove(q)
        except ValueError:
            pass

    async def emit(self, event: Event) -> None:
        self._history.append(event)
        if len(self._history) > self._buffer_size:
            self._history = self._history[-self._buffer_size:]
        for q in list(self._subscribers):
            try:
                q.put_nowait(event)
            except asyncio.QueueFull:
                pass

# Singleton (Orchestrator und Server teilen sich den Bus)
_bus: EventBus | None = None

def get_bus() -> EventBus:
    global _bus
    if _bus is None:
        _bus = EventBus()
    return _bus
