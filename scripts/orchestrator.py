"""Phasen-Orchestrator. In M16 wird der volle Ablauf integriert."""
from __future__ import annotations
from scripts.event_bus import Event, get_bus
from scripts.utils import log

async def start_orchestrator(topic: str, rahmen: str) -> None:
    bus = get_bus()
    await bus.emit(Event(type="phase", data={"phase": 1, "status": "running", "name": "Rubrik-Ingestion"}))
    log.info(f"Orchestrator started: topic={topic}, rahmen={rahmen}")
    # Wird in M16 mit echter Logik befüllt.
