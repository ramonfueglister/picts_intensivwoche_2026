import asyncio
import pytest
from scripts.event_bus import EventBus, Event

@pytest.mark.asyncio
async def test_emit_and_receive():
    bus = EventBus()
    sub = bus.subscribe()
    await bus.emit(Event(type="phase", data={"phase": 1, "status": "running"}))
    evt = await asyncio.wait_for(sub.get(), timeout=0.5)
    assert evt.type == "phase"
    assert evt.data["phase"] == 1

@pytest.mark.asyncio
async def test_multiple_subscribers():
    bus = EventBus()
    s1, s2 = bus.subscribe(), bus.subscribe()
    await bus.emit(Event(type="test", data={"x": 1}))
    e1 = await asyncio.wait_for(s1.get(), timeout=0.5)
    e2 = await asyncio.wait_for(s2.get(), timeout=0.5)
    assert e1.data == e2.data == {"x": 1}
