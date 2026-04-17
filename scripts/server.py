"""FastAPI-App: statisches Frontend + SSE-Stream + Artifact-Downloads."""
from __future__ import annotations
import asyncio
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse

from scripts import config
from scripts.event_bus import get_bus

app = FastAPI(title="VA-Agent")

WEB_DIR = Path(__file__).parent / "web"

_state: dict = {"state": "idle", "phase": 0, "cost_usd": 0.0}

def set_state(**kwargs):
    _state.update(kwargs)

def get_state() -> dict:
    return dict(_state)

@app.get("/")
async def root():
    index = WEB_DIR / "index.html"
    if index.exists():
        return FileResponse(index)
    return JSONResponse({"msg": "VA-Agent läuft (Frontend noch nicht gebaut)"}, status_code=200)

@app.get("/api/status")
async def api_status():
    return get_state()

@app.get("/api/score")
async def api_score():
    import json
    from pathlib import Path
    p = config.OUTPUT_DIR / "score_report.json"
    if not p.exists():
        return {"ready": False}
    return {"ready": True, **json.loads(p.read_text(encoding="utf-8"))}

@app.get("/api/stream")
async def api_stream():
    bus = get_bus()
    queue = bus.subscribe(replay_history=True)

    async def gen():
        try:
            while True:
                evt = await queue.get()
                yield {"event": evt.type, "data": evt.to_json()}
        except asyncio.CancelledError:
            bus.unsubscribe(queue)
            raise

    return EventSourceResponse(gen())

@app.post("/api/start")
async def api_start(body: dict):
    from scripts.orchestrator import start_orchestrator
    if _state["state"] == "running":
        raise HTTPException(409, "already running")
    set_state(state="running", phase=1)
    asyncio.create_task(start_orchestrator(
        topic=body.get("topic", config.VA_AGENT_TOPIC),
        rahmen=body.get("rahmen", config.VA_AGENT_RAHMEN),
    ))
    return {"ok": True}

@app.get("/api/artifacts")
async def api_artifacts():
    if not config.ARTIFACTS_DIR.exists():
        return []
    items = []
    for f in sorted(config.ARTIFACTS_DIR.iterdir()):
        if f.is_file():
            items.append({"id": f.stem, "filename": f.name, "size": f.stat().st_size})
    return items

@app.get("/api/artifacts/{filename}")
async def api_artifact(filename: str):
    path = config.ARTIFACTS_DIR / filename
    if not path.exists() or not path.is_file():
        raise HTTPException(404, "not found")
    return FileResponse(path)

@app.get("/api/zip")
async def api_zip():
    import zipfile
    import io
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in config.ARTIFACTS_DIR.iterdir():
            if f.is_file():
                zf.write(f, arcname=f.name)
    buf.seek(0)
    zip_path = config.OUTPUT_DIR / "va_komplett.zip"
    zip_path.write_bytes(buf.getvalue())
    return FileResponse(zip_path, media_type="application/zip", filename="va_komplett.zip")

if WEB_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")
