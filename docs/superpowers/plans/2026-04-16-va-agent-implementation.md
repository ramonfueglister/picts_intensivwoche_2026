# VA-Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Standalone-Web-App, die in 20-25 Min eine komplette Vertiefungsarbeit (18 Artefakte, Wegleitung-konform) für fiktiven FaGe-Lernenden produziert und als Shock-Demo im 30-Min-PICTS-Slot läuft.

**Architecture:** Python/FastAPI-Backend mit asyncio-Orchestrator, der 15 Subagenten (Claude Opus/Sonnet, ElevenLabs, Runway, Hedra, FLUX) seriell + parallel steuert. Vanilla-JS-Frontend mit SSE-Stream zeigt Live-Progress. Alle Artefakte in `_output/agent/artifacts/`, auf `localhost:8001/` im Browser zugänglich.

**Tech Stack:** Python 3.11+, FastAPI, uvicorn, sse-starlette, anthropic SDK, elevenlabs, fal-client (FLUX), runwayml, httpx, pdfplumber, WeasyPrint, python-pptx, matplotlib, Jinja2, pytest.

**Spec:** [docs/superpowers/specs/2026-04-16-va-agent-design.md](../specs/2026-04-16-va-agent-design.md)

**Zeitrahmen:** 18:00 Do 16.04. → 07:30 Fr 17.04. (~13.5h). Checkpoint-Zeiten sind im Plan vermerkt.

---

## File Structure

### Neue Dateien (scripts/)

```
scripts/
├── __init__.py
├── agent_va.py                ← CLI-Entry (python -m scripts.agent_va)
├── server.py                  ← FastAPI-App
├── orchestrator.py            ← Phasen-Steuerung, asyncio.gather
├── coherence.py               ← Universum-Management
├── rubric_parser.py           ← Wegleitung-PDF → rubric.json
├── event_bus.py               ← asyncio.Queue für SSE
├── config.py                  ← Settings aus .env
├── utils.py                   ← logger, retry, atomic-write
├── subagents/
│   ├── __init__.py
│   ├── base.py                ← Shared subagent protocol
│   ├── konzept.py
│   ├── literatur.py
│   ├── interview.py
│   ├── audio.py
│   ├── video.py
│   ├── foto.py
│   ├── umfrage.py
│   ├── journal.py
│   ├── reflexion.py
│   ├── email.py
│   ├── formular.py
│   ├── praesentation.py
│   ├── haupttext.py
│   ├── redaktor.py
│   └── self_check.py
├── media/
│   ├── __init__.py
│   ├── tts_elevenlabs.py      ← Voice Clone + Synthesize
│   ├── video_runway.py        ← B-Roll-Generator
│   ├── video_hedra.py         ← Lip-Sync-Avatar
│   ├── image_flux.py          ← FLUX 1.2 Pro via fal
│   ├── signature_svg.py       ← Perlin-Noise-Unterschriften
│   └── pdf_render.py          ← WeasyPrint Wrapper
├── tools/                     ← HTTP-Tools für Literatur-Agent
│   ├── __init__.py
│   ├── openalex.py
│   ├── google_books.py
│   ├── pubmed.py
│   └── srf_fetch.py
└── web/
    ├── index.html
    ├── app.js
    └── style.css

templates/
├── va_html.j2                 ← Haupttext Master
├── va_css.css                 ← Arial 11, LS 1.5
├── konzept_html.j2
├── journal_html.j2
├── zwischenreflexion_html.j2
├── gesamtreflexion_html.j2
├── eigenstaendigkeit_html.j2
├── einverstaendnis_html.j2
├── titelblatt_html.j2
└── umfrage_fragebogen_html.j2

scripts/prompts/               ← Jinja2-Prompts für LLM
├── konzept.j2
├── literatur_search_plan.j2
├── interview_leitfaden.j2
├── interview_transkript.j2
├── umfrage_fragebogen.j2
├── umfrage_antworten.j2
├── journal_woche.j2
├── zwischenreflexion.j2
├── gesamtreflexion.j2
├── email_draft.j2
├── praesentation_slides.j2
├── haupttext_kapitel.j2
├── redaktor.j2
├── self_check.j2
└── universum_komposition.j2

tests/
├── __init__.py
├── test_coherence.py
├── test_rubric_parser.py
├── test_event_bus.py
├── test_signature_svg.py
├── test_pdf_render.py
└── test_smoke_server.py

_output/agent/                 ← Runtime-Output, nicht in git
├── status.json
├── universe.json
├── rubric.json
├── score_report.json
├── artifacts/
└── prerendered/
```

### Neue Konfigurations-Dateien

```
.env.example                   ← Template mit API-Key-Slots
pyproject.toml                 ← Dependencies (MODIFY bestehende)
.gitignore                     ← _output/agent/* hinzufügen (MODIFY)
```

---

## Milestones Overview

| M | Titel | Dauer | Bis |
|---|---|---|---|
| 1 | Projekt-Setup (pyproject, .env, scaffold) | 30m | 18:30 |
| 2 | Event Bus + SSE Foundation | 30m | 19:00 |
| 3 | Voice-Klon aufnehmen + ElevenLabs Upload | 30m | 19:30 |
| 4 | Coherence Manager + Universe Schema | 30m | 20:00 |
| 5 | Rubric Parser | 20m | 20:20 |
| 6 | Konzept-Agent (Pattern-Setter) | 45m | 21:05 |
| 7 | Literatur-Agent (4 HTTP-Tools) | 45m | 21:50 |
| 8 | Interview + Audio-Agent | 45m | 22:35 |
| 9 | Video-Agent (Runway + Hedra) | 45m | 23:20 |
| 10 | Foto-Agent (FLUX) | 20m | 23:40 |
| 11 | Umfrage-Agent (mit Plots) | 30m | 00:10 |
| 12 | Journal + Reflexion + E-Mail + Formular | 45m | 00:55 |
| 13 | Präsentations-Agent (pptx) | 30m | 01:25 |
| 14 | Haupttext + Redaktor + Self-Check | 45m | 02:10 |
| 15 | PDF-Render + ZIP-Bundle | 30m | 02:40 |
| 16 | Orchestrator-Integration + Phasen-Wiring | 45m | 03:25 |
| 17 | Frontend (drei Screens + SSE-Client) | 60m | 04:25 |
| 18 | End-to-End Dry-Run 1 + Fixes | 60m | 05:25 |
| 19 | Pre-Rendered-Fallback + .env-Flag | 30m | 05:55 |
| 20 | Dry-Run 2 + Polish + Sleep-Buffer | 90m | 07:25 |

**Total:** ~13h mit Puffer. Morgen 07:30 Generalprobe vor Ort.

---

## Milestone 1: Projekt-Setup (30m · bis 18:30)

### Task 1.1: pyproject.toml erweitern

**Files:**
- Modify: `pyproject.toml` (falls existiert, sonst Create)

- [ ] **Step 1: Check ob pyproject.toml existiert**

Run: `ls pyproject.toml`

Wenn existiert: Dependencies mergen. Wenn nicht: neu anlegen.

- [ ] **Step 2: pyproject.toml schreiben/erweitern**

```toml
[project]
name = "va-agent"
version = "0.1.0"
description = "VA-Agent Demo für PICTS 17.04.2026"
requires-python = ">=3.11"
dependencies = [
    "anthropic>=0.60.0",
    "elevenlabs>=2.0.0",
    "fal-client>=0.4.0",
    "runwayml>=3.0.0",
    "httpx>=0.27.0",
    "fastapi>=0.110.0",
    "uvicorn[standard]>=0.30.0",
    "sse-starlette>=2.0.0",
    "python-multipart",
    "pdfplumber>=0.11.0",
    "weasyprint>=62.0",
    "python-pptx>=1.0.0",
    "pandas>=2.2.0",
    "matplotlib>=3.9.0",
    "numpy>=2.0.0",
    "jinja2>=3.1.0",
    "python-dotenv",
    "pydantic>=2.0",
    "rich",
    "ffmpeg-python>=0.2.0",
    "Pillow>=10.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "pytest-httpx>=0.30",
]

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["."]
include = ["scripts*"]
```

- [ ] **Step 3: venv anlegen + installieren**

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Expected: Erfolgreiche Installation aller Deps. Bei WeasyPrint-Fehler auf macOS: `brew install pango cairo gdk-pixbuf libffi`.

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml
git commit -m "chore: va-agent dependencies"
```

### Task 1.2: .env.example + .env anlegen

**Files:**
- Create: `.env.example`
- Create: `.env` (nicht committen, steht in .gitignore)

- [ ] **Step 1: .env.example schreiben**

```
# Claude
ANTHROPIC_API_KEY=sk-ant-...

# ElevenLabs
ELEVENLABS_API_KEY=sk_...
ELEVENLABS_VOICE_ID_LUCA=              # wird in M3 gesetzt
ELEVENLABS_VOICE_ID_DRWEBER=elsa       # Preset-Name

# Runway
RUNWAYML_API_KEY=...

# Hedra
HEDRA_API_KEY=...

# FAL (für FLUX)
FAL_KEY=...

# App
VA_AGENT_PORT=8001
USE_PRERENDERED=0
VA_AGENT_TOPIC="Einsamkeit im Alter — Wie Spitex-Fachleute sie erkennen und ihr begegnen"
VA_AGENT_RAHMEN="Gegensätze"
```

- [ ] **Step 2: .env kopieren und echte Keys eintragen**

```bash
cp .env.example .env
# Nun .env öffnen und echte Keys reinschreiben
```

- [ ] **Step 3: .gitignore prüfen**

```bash
grep -q "^\.env$" .gitignore || echo ".env" >> .gitignore
grep -q "^_output/agent/" .gitignore || echo "_output/agent/" >> .gitignore
```

- [ ] **Step 4: Commit**

```bash
git add .env.example .gitignore
git commit -m "chore: env template + gitignore updates"
```

### Task 1.3: Directory-Scaffold anlegen

**Files:**
- Create: `scripts/__init__.py` (leer)
- Create: `scripts/subagents/__init__.py` (leer)
- Create: `scripts/media/__init__.py` (leer)
- Create: `scripts/tools/__init__.py` (leer)
- Create: `tests/__init__.py` (leer)
- Create: `templates/.gitkeep`
- Create: `scripts/prompts/.gitkeep`
- Create: `scripts/web/.gitkeep`

- [ ] **Step 1: Directories + leere __init__.py**

```bash
mkdir -p scripts/{subagents,media,tools,prompts,web} tests templates _output/agent/{artifacts,prerendered}
touch scripts/__init__.py scripts/subagents/__init__.py scripts/media/__init__.py scripts/tools/__init__.py tests/__init__.py templates/.gitkeep scripts/prompts/.gitkeep scripts/web/.gitkeep
```

- [ ] **Step 2: Commit**

```bash
git add scripts tests templates
git commit -m "chore: scaffold project dirs"
```

### Task 1.4: config.py — Settings aus .env

**Files:**
- Create: `scripts/config.py`

- [ ] **Step 1: config.py schreiben**

```python
"""Runtime-Settings, aus .env geladen via python-dotenv."""
from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "_output" / "agent"
ARTIFACTS_DIR = OUTPUT_DIR / "artifacts"
PRERENDERED_DIR = OUTPUT_DIR / "prerendered"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
PROMPTS_DIR = PROJECT_ROOT / "scripts" / "prompts"
WEGLEITUNG_PDF = Path.home() / "Desktop" / "ABU_VA_Wegleitung_FaGe_Version12_2025.pdf"

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID_LUCA = os.getenv("ELEVENLABS_VOICE_ID_LUCA", "")
ELEVENLABS_VOICE_ID_DRWEBER = os.getenv("ELEVENLABS_VOICE_ID_DRWEBER", "elsa")
RUNWAYML_API_KEY = os.getenv("RUNWAYML_API_KEY")
HEDRA_API_KEY = os.getenv("HEDRA_API_KEY")
FAL_KEY = os.getenv("FAL_KEY")
VA_AGENT_PORT = int(os.getenv("VA_AGENT_PORT", "8001"))
USE_PRERENDERED = os.getenv("USE_PRERENDERED", "0") == "1"
VA_AGENT_TOPIC = os.getenv("VA_AGENT_TOPIC", "Einsamkeit im Alter")
VA_AGENT_RAHMEN = os.getenv("VA_AGENT_RAHMEN", "Gegensätze")

CLAUDE_MODEL_OPUS = "claude-opus-4-6"
CLAUDE_MODEL_SONNET = "claude-sonnet-4-6"

def ensure_dirs():
    for d in (OUTPUT_DIR, ARTIFACTS_DIR, PRERENDERED_DIR):
        d.mkdir(parents=True, exist_ok=True)

ensure_dirs()
```

- [ ] **Step 2: utils.py mit Logger + retry**

Create: `scripts/utils.py`

```python
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
```

- [ ] **Step 3: Smoke-Import-Test**

```bash
python -c "from scripts import config, utils; print(config.OUTPUT_DIR)"
```

Expected: Pfad wird ausgegeben, keine Exception.

- [ ] **Step 4: Commit**

```bash
git add scripts/config.py scripts/utils.py
git commit -m "feat: config loader + logging/retry utils"
```

---

## Milestone 2: Event Bus + SSE Foundation (30m · bis 19:00)

### Task 2.1: event_bus.py

**Files:**
- Create: `scripts/event_bus.py`
- Create: `tests/test_event_bus.py`

- [ ] **Step 1: Test schreiben**

```python
# tests/test_event_bus.py
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
```

- [ ] **Step 2: Test laufen (fehlschlägt)**

```bash
pytest tests/test_event_bus.py -v
```

Expected: FAIL — `EventBus`/`Event` nicht importierbar.

- [ ] **Step 3: event_bus.py implementieren**

```python
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
```

- [ ] **Step 4: Test grün**

```bash
pytest tests/test_event_bus.py -v
```

Expected: PASS 2/2.

- [ ] **Step 5: Commit**

```bash
git add scripts/event_bus.py tests/test_event_bus.py
git commit -m "feat: EventBus with history replay for SSE"
```

### Task 2.2: FastAPI-Skeleton mit SSE-Endpoint

**Files:**
- Create: `scripts/server.py`
- Create: `tests/test_smoke_server.py`

- [ ] **Step 1: Smoke-Test schreiben**

```python
# tests/test_smoke_server.py
from fastapi.testclient import TestClient
from scripts.server import app

def test_root_returns_html():
    client = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200
    assert "VA-Agent" in r.text

def test_status_initial():
    client = TestClient(app)
    r = client.get("/api/status")
    assert r.status_code == 200
    assert "state" in r.json()
```

- [ ] **Step 2: server.py implementieren**

```python
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
```

- [ ] **Step 3: Stub-Orchestrator für Smoke-Test**

Create: `scripts/orchestrator.py` (Stub)

```python
"""Phasen-Orchestrator. In M16 wird der volle Ablauf integriert."""
from __future__ import annotations
from scripts.event_bus import Event, get_bus
from scripts.utils import log

async def start_orchestrator(topic: str, rahmen: str) -> None:
    bus = get_bus()
    await bus.emit(Event(type="phase", data={"phase": 1, "status": "running", "name": "Rubrik-Ingestion"}))
    log.info(f"Orchestrator started: topic={topic}, rahmen={rahmen}")
    # Wird in M16 mit echter Logik befüllt.
```

- [ ] **Step 4: Stub index.html**

Create: `scripts/web/index.html`

```html
<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><title>VA-Agent</title></head>
<body><h1>VA-Agent läuft</h1><p>Frontend kommt in M17.</p></body></html>
```

- [ ] **Step 5: Test grün**

```bash
pytest tests/test_smoke_server.py -v
```

Expected: PASS 2/2.

- [ ] **Step 6: Server manuell testen**

```bash
uvicorn scripts.server:app --host 127.0.0.1 --port 8001 --reload &
sleep 2
curl http://127.0.0.1:8001/api/status
kill %1
```

Expected: `{"state":"idle","phase":0,"cost_usd":0.0}`

- [ ] **Step 7: Commit**

```bash
git add scripts/server.py scripts/orchestrator.py scripts/web/index.html tests/test_smoke_server.py
git commit -m "feat: FastAPI skeleton + SSE + artifact endpoints"
```

---

## Milestone 3: Voice-Klon aufnehmen (30m · bis 19:30)

**Nicht-Code-Schritte. Ramon macht das am Mikrofon.**

### Task 3.1: Aufnahme + Upload

- [ ] **Step 1: QuickTime Player öffnen → Neue Audioaufnahme → Mikrofon "MacBook eingebaut" oder "AirPods Pro"**

- [ ] **Step 2: 90-120 Sekunden vorlesen**

Text (neutral, ohne persönliche Angaben — z.B. Wegleitung-Auszug):

> "Die Generierung von Texten oder gestalterischen Werken mit Hilfe von KI kann als ein Prozess der Ko-Kreation von Mensch und Maschine aufgefasst werden, der Mensch behält jedoch immer die Verantwortung für den Text und das Werk. Sie als Verfasser, als Verfasserin sind somit sowohl für die generierten Inhalte und den Faktencheck als auch für die Einhaltung von urheberrechtlichen Bestimmungen sowie die wissenschaftliche Integrität ihres Produktes verantwortlich. Im Sinne der Eigenleistung bzw. wissenschaftlichen Integrität muss die Verwendung von KI transparent gemacht werden."

Natürliche Intonation, etwas Varianz (Frage hochheben, Satzende absenken, leichter Rhythmus).

- [ ] **Step 3: Speichern als `luca_voice_sample.m4a` oder `.wav` in `~/Desktop/`**

- [ ] **Step 4: Zu ElevenLabs Dashboard gehen**

https://elevenlabs.io/app/voice-lab → "Add Voice" → "Professional Voice Clone"

- [ ] **Step 5: Upload + Namensgebung**

Name: `Luca_Brunner_VA_Agent_2026_04_17`
Description: "Demo-Stimme für PICTS-Talk 17.04.2026 — Ramons Klon. Nach Talk löschen."

- [ ] **Step 6: Warten auf Processing (~5-10 Min)**

Während des Wartens: bereits mit M4 weitermachen.

- [ ] **Step 7: Voice-ID kopieren, in .env eintragen**

```bash
# .env öffnen, ELEVENLABS_VOICE_ID_LUCA=xyz... setzen
```

- [ ] **Step 8: Test-Synthese**

Create: `scripts/dev_test_voice.py`

```python
"""Einmaliger Dev-Test: hört die geklonte Stimme einen Testsatz sprechen?"""
from elevenlabs.client import ElevenLabs
from scripts import config
from pathlib import Path

client = ElevenLabs(api_key=config.ELEVENLABS_API_KEY)
audio = client.text_to_speech.convert(
    voice_id=config.ELEVENLABS_VOICE_ID_LUCA,
    model_id="eleven_multilingual_v2",
    text="Grüezi Frau Doktor Weber, mein Name ist Luca Brunner. Ich mache gerade meine Vertiefungsarbeit zum Thema Einsamkeit im Alter.",
    output_format="mp3_44100_128",
)
out = Path("_output/agent/voice_test_luca.mp3")
out.parent.mkdir(parents=True, exist_ok=True)
with out.open("wb") as f:
    for chunk in audio:
        f.write(chunk)
print(f"✅ {out}")
```

```bash
python scripts/dev_test_voice.py
open _output/agent/voice_test_luca.mp3
```

Expected: Abspielbare Audiodatei, die wie Ramon klingt.

- [ ] **Step 9: Falls Qualität schlecht**

Längere Aufnahme (2-3 Min), mehr Intonationsvariation, ruhigere Umgebung. Voice neu erstellen, alte Voice-ID löschen, neue ID in `.env`.

- [ ] **Step 10: NICHT committen**

`.env` ist in `.gitignore`. `dev_test_voice.py` kann committed werden, ist harmlos.

```bash
git add scripts/dev_test_voice.py
git commit -m "chore: voice clone test script"
```

---

## Milestone 4: Coherence Manager + Universe Schema (30m · bis 20:00)

### Task 4.1: Pydantic-Modelle für Universe

**Files:**
- Create: `scripts/coherence.py`
- Create: `tests/test_coherence.py`

- [ ] **Step 1: Test schreiben**

```python
# tests/test_coherence.py
from pathlib import Path
from scripts.coherence import Universe, load_universe, save_universe, validate_artifact_text

def test_universe_roundtrip(tmp_path):
    u = Universe.sample()
    p = tmp_path / "u.json"
    save_universe(u, p)
    loaded = load_universe(p)
    assert loaded.schuelerin.vorname == u.schuelerin.vorname
    assert loaded.interviewperson.name_anzeige == u.interviewperson.name_anzeige

def test_validate_artifact_detects_wrong_name():
    u = Universe.sample()
    text = "Das Interview mit Dr. Müller war spannend."
    issues = validate_artifact_text("test.txt", text, u)
    assert any("Dr. Müller" in i or "name" in i.lower() for i in issues)

def test_validate_artifact_accepts_correct():
    u = Universe.sample()
    text = f"Das Interview mit {u.interviewperson.name_anzeige} war spannend."
    issues = validate_artifact_text("test.txt", text, u)
    assert issues == []
```

- [ ] **Step 2: Test fehlschlägt**

```bash
pytest tests/test_coherence.py -v
```

Expected: FAIL — `Universe` nicht importierbar.

- [ ] **Step 3: coherence.py implementieren**

```python
"""Fiktiv-Universum: Single Source of Truth für alle Subagenten."""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Literal
from pydantic import BaseModel, Field

from scripts import config
from scripts.utils import atomic_write_json, log

class Thema(BaseModel):
    rahmen: str
    titel: str
    aspekte: list[str]
    methoden: list[str]

class Schuelerin(BaseModel):
    vorname: str
    nachname: str
    pronomen: Literal["er", "sie", "they"]
    klasse: str
    geburtsdatum: str
    lehrbetrieb: str
    lehrperson: str
    schule: str
    voice_id_elevenlabs: str
    schreibstil_marker: list[str]

class Interviewperson(BaseModel):
    name_anzeige: str
    funktion: str
    alter: int
    email_fiktiv: str
    foto_prompt: str
    tts_voice_id: str
    interview_termin: str
    urspruenglicher_termin_abgesagt: str

class Umfrage(BaseModel):
    plattform: str
    url_anzeige: str
    zeitraum: str
    n_versendet: int
    n_ruecklauf: int

class TimelineEintrag(BaseModel):
    woche: int
    datum_start: str
    highlights: str
    journal_laenge: str

class Quelle(BaseModel):
    typ: Literal["buch", "fachartikel", "zeitungsartikel", "internet", "podcast", "dokumentarfilm"]
    autor: str
    titel: str
    jahr: int | None = None
    verlag: str | None = None
    isbn: str | None = None
    doi: str | None = None
    url: str | None = None
    kapitel_zuordnung: str | None = None  # "Einleitung", "Kap. 2", etc.
    snippet: str | None = None
    real_verified: bool = False
    api_source: str | None = None

class Universe(BaseModel):
    thema: Thema
    schuelerin: Schuelerin
    interviewperson: Interviewperson
    umfrage: Umfrage
    timeline: list[TimelineEintrag]
    quellen: list[Quelle] = Field(default_factory=list)
    konsistenz_regeln: list[str] = Field(default_factory=list)

    @classmethod
    def sample(cls) -> "Universe":
        """Canonical starting universe — wird von Orchestrator beim Start erzeugt."""
        return cls(
            thema=Thema(
                rahmen=config.VA_AGENT_RAHMEN,
                titel=config.VA_AGENT_TOPIC,
                aspekte=["Identität & Sozialisation", "Ethik", "Gender"],
                methoden=["Fachinterview", "Umfrage"],
            ),
            schuelerin=Schuelerin(
                vorname="Luca",
                nachname="Brunner",
                pronomen="er",
                klasse="FaGe 24b",
                geburtsdatum="2006-08-14",
                lehrbetrieb="Spitex Zürich Limmat, Standort Seefeld",
                lehrperson="Martina Keller",
                schule="ZAG Winterthur",
                voice_id_elevenlabs=config.ELEVENLABS_VOICE_ID_LUCA,
                schreibstil_marker=[
                    "gelegentlich etwas lange Sätze",
                    "verwendet gern 'eigentlich' und 'einfach'",
                    "gendert konsequent mit Doppelpunkt",
                    "ab und zu ein Rechtschreibfehler, der bewusst bleibt",
                    "persönliche Anekdoten aus dem Praktikum",
                ],
            ),
            interviewperson=Interviewperson(
                name_anzeige="Dr. phil. Andrea Weber",
                funktion="Dozentin für Pflegewissenschaft, ZHAW Departement Gesundheit",
                alter=52,
                email_fiktiv="a.weber@example.ch",
                foto_prompt="50-jährige Pflegewissenschaftlerin, warme Ausstrahlung, Brille, kurze graumelierte Haare, helles Büro mit Bücherregal im Hintergrund, Porträt, natürliches Licht",
                tts_voice_id=config.ELEVENLABS_VOICE_ID_DRWEBER,
                interview_termin="2026-02-20",
                urspruenglicher_termin_abgesagt="2026-02-14",
            ),
            umfrage=Umfrage(
                plattform="umfrageonline.ch",
                url_anzeige="https://umfrageonline.ch/s/luca-va-2026",
                zeitraum="2026-01-15 bis 2026-02-05",
                n_versendet=85,
                n_ruecklauf=52,
            ),
            timeline=[
                TimelineEintrag(woche=1, datum_start="2025-12-01", highlights="Thema festgelegt, Mindmap erstellt", journal_laenge="normal"),
                TimelineEintrag(woche=2, datum_start="2025-12-08", highlights="Konzept begonnen, 3 Ziele formuliert", journal_laenge="normal"),
                TimelineEintrag(woche=3, datum_start="2025-12-15", highlights="Konzept überarbeitet nach Zwischengespräch", journal_laenge="normal"),
                TimelineEintrag(woche=4, datum_start="2025-12-22", highlights="Pause Weihnachten, Umfrage vorbereitet", journal_laenge="kurz, gestresst"),
                TimelineEintrag(woche=5, datum_start="2026-01-12", highlights="Umfrage versendet, Dr. Meier sagt ab", journal_laenge="frustriert"),
                TimelineEintrag(woche=6, datum_start="2026-01-19", highlights="Dr. Weber hat zugesagt, Erleichterung", journal_laenge="erleichtert"),
                TimelineEintrag(woche=7, datum_start="2026-01-26", highlights="Umfrage ausgewertet, Einleitung begonnen", journal_laenge="lang"),
                TimelineEintrag(woche=8, datum_start="2026-02-02", highlights="Interview durchgeführt, Haupttext begonnen", journal_laenge="lang"),
            ],
            quellen=[],
            konsistenz_regeln=[
                "Alle Daten in 2025/2026 (nicht vor 2025-12-01)",
                "Interviewpersonen-Name 'Dr. phil. Andrea Weber' oder 'Dr. Weber' überall gleich",
                "Voice-ID der Schüler-Stimme konsistent über Interview-Audio",
                "Quellen im Quellenverzeichnis mit Kapitel-Zuordnung",
                "Mindestens 2 Quellen CH-spezifisch",
                "Projektjournal enthält Dr.-Meier-Absage 14.02.2026",
            ],
        )


def load_universe(path: Path = config.OUTPUT_DIR / "universe.json") -> Universe:
    with path.open("r", encoding="utf-8") as f:
        return Universe.model_validate_json(f.read())

def save_universe(u: Universe, path: Path = config.OUTPUT_DIR / "universe.json") -> None:
    atomic_write_json(path, u.model_dump(mode="json"))
    log.info(f"Universe gespeichert: {path}")

# Verbotene Namen (Common hallucinated alternatives)
_FORBIDDEN_NAMES = ["Müller", "Meyer", "Fischer", "Schmidt", "Sarah Chen"]

def validate_artifact_text(name: str, text: str, u: Universe) -> list[str]:
    """Prüft ein Artefakt gegen das Universe. Liefert Liste von Problemen."""
    issues: list[str] = []
    correct_name = u.interviewperson.name_anzeige
    short_name = correct_name.split()[-1]  # "Weber"
    for fn in _FORBIDDEN_NAMES:
        if fn in text and fn not in correct_name:
            issues.append(f"{name}: verbotener Name 'Dr. {fn}' gefunden (korrekt: {correct_name})")
    # Jahr-Check: Daten müssen 2025/2026 sein
    for bad_year in ["2023", "2024"]:
        if bad_year in text:
            issues.append(f"{name}: altes Jahr {bad_year} gefunden (Timeline ist 2025/2026)")
    return issues
```

- [ ] **Step 4: Test grün**

```bash
pytest tests/test_coherence.py -v
```

Expected: PASS 3/3.

- [ ] **Step 5: Commit**

```bash
git add scripts/coherence.py tests/test_coherence.py
git commit -m "feat: Universe pydantic model + coherence validator"
```

---

## Milestone 5: Rubric Parser (20m · bis 20:20)

### Task 5.1: Rubric-Parser für Wegleitung-PDF

**Files:**
- Create: `scripts/rubric_parser.py`
- Create: `tests/test_rubric_parser.py`

Weil die PDF-Struktur kompliziert und zeitaufwändig zu parsen ist, verwenden wir einen **Hybrid-Ansatz**: hart-kodierte Rubric-Struktur (aus Wegleitung S. 23-25 abgelesen) + optionaler PDF-Sanity-Check.

- [ ] **Step 1: Test schreiben**

```python
# tests/test_rubric_parser.py
from scripts.rubric_parser import load_rubric, Rubric

def test_rubric_has_120_points():
    r = load_rubric()
    total = r.teile["A_prozess"].max + r.teile["B_produkt"].max + r.teile["C_praesentation"].max
    assert total == 120

def test_konzeptbeschrieb_has_9_points():
    r = load_rubric()
    kriterien = {k.name: k for k in r.teile["A_prozess"].kriterien}
    assert kriterien["Konzeptbeschrieb"].max == 9

def test_notenskala_5_at_90():
    r = load_rubric()
    # Suche: bei 90 Punkten muss Note 5.0 sein
    for punkte, note in r.notenskala:
        if punkte == 90:
            assert note == 5.0
            return
    raise AssertionError("Keine Eintrag 90 Punkte in Notenskala")
```

- [ ] **Step 2: rubric_parser.py implementieren**

```python
"""Rubric-Parser: Wegleitung S. 23-25 → strukturierte Rubrik."""
from __future__ import annotations
from pydantic import BaseModel, Field
from pathlib import Path
import json
from scripts import config
from scripts.utils import atomic_write_json

class SubKriterium(BaseModel):
    text: str
    p: int  # Punkte

class Kriterium(BaseModel):
    name: str
    max: int
    sub: list[SubKriterium] = Field(default_factory=list)
    assigned_artifact: str | None = None  # welches Artefakt deckt das ab

class Teil(BaseModel):
    name: str
    max: int
    kriterien: list[Kriterium]

class Rubric(BaseModel):
    teile: dict[str, Teil]
    notenskala: list[tuple[int, float]]

_RUBRIC_JSON: dict = {
    "teile": {
        "A_prozess": {
            "name": "A Prozess",
            "max": 30,
            "kriterien": [
                {
                    "name": "Konzeptbeschrieb",
                    "max": 9,
                    "sub": [
                        {"text": "Themenbegründung mit Bezug zum VA-Oberthema", "p": 1},
                        {"text": "Persönlicher Bezug hergestellt", "p": 1},
                        {"text": "Verweis auf Wissenszuwachs", "p": 1},
                        {"text": "Bezug zu mindestens 2 Aspekten/Blickwinkeln", "p": 2},
                        {"text": "Zielformulierungen realisierbar und vorausschauend auf konkrete Tätigkeiten", "p": 3},
                        {"text": "Passende Methoden (mind. 2) gewählt", "p": 2},
                    ],
                    "assigned_artifact": "02_konzept.pdf",
                },
                {
                    "name": "Projektjournal",
                    "max": 6,
                    "sub": [
                        {"text": "Wöchentliche Auskunft über Tätigkeiten", "p": 3},
                        {"text": "Reflektiert an zwei vorgegebenen Daten ausführlich", "p": 3},
                    ],
                    "assigned_artifact": "06_projektjournal.pdf",
                },
                {
                    "name": "Reflexion Arbeitsprozess",
                    "max": 6,
                    "sub": [
                        {"text": "Mindestens ¾ A4 zusammenhängend gegliedert", "p": 1},
                        {"text": "Ausführlich positive und negative Erfahrungen", "p": 1},
                        {"text": "Planung und Zeitmanagement", "p": 1},
                        {"text": "Zusammenarbeit / Organisation", "p": 1},
                        {"text": "Erkennen und Lösen von Schwierigkeiten", "p": 1},
                        {"text": "Was würde nächstes Mal anders", "p": 1},
                    ],
                    "assigned_artifact": "09_gesamtreflexion.pdf",
                },
                {
                    "name": "Zwischenpräsentation",
                    "max": 6,
                    "sub": [
                        {"text": "Deutlicher Einblick zum Zwischenstand", "p": 4},
                        {"text": "Verbal, nonverbal, medial überzeugend", "p": 2},
                    ],
                    "assigned_artifact": "18_zwischenpraesentation.pptx",
                },
                {
                    "name": "Lehrperson Arbeitsprozess",
                    "max": 3,
                    "sub": [
                        {"text": "Termine eingehalten", "p": 1},
                        {"text": "Geforderte Unterlagen vorhanden", "p": 1},
                        {"text": "Probleme rechtzeitig besprochen, Lösungen angestrebt", "p": 1},
                    ],
                    "assigned_artifact": None,  # nicht automatisierbar
                },
            ],
        },
        "B_produkt": {
            "name": "B Produkt",
            "max": 50,
            "kriterien": [
                {
                    "name": "Formale Kriterien / Titelblatt / Inhaltsverzeichnis",
                    "max": 8,
                    "sub": [
                        {"text": "Darstellung ansprechend, übersichtlich, sorgfältig", "p": 2},
                        {"text": "Umfang entspricht Vorgaben inkl. Anhang", "p": 3},
                        {"text": "Titelblatt vollständig und gut gestaltet", "p": 1},
                        {"text": "Inhaltsverzeichnis logisch, systematisch, mit Seitenzahlen", "p": 1},
                        {"text": "Aussagekräftige Kapitelüberschriften", "p": 1},
                    ],
                    "assigned_artifact": "03_va_hauptarbeit.pdf",
                },
                {
                    "name": "Einleitung",
                    "max": 6,
                    "sub": [
                        {"text": "Zusammenhang des Themas zum Rahmenthema", "p": 1},
                        {"text": "Begründung der Themenwahl allgemein und persönlich", "p": 2},
                        {"text": "Zielformulierungen zu mind. 2 Aspekten", "p": 2},
                        {"text": "Inhaltlicher Aufbau / Methoden beschrieben", "p": 1},
                    ],
                    "assigned_artifact": "03_va_hauptarbeit.pdf",
                },
                {
                    "name": "Haupttext Inhalt",
                    "max": 8,
                    "sub": [
                        {"text": "Inhalt sachlich richtig, mit erkennbarem Fachwissen", "p": 3},
                        {"text": "Berücksichtigt Zielformulierungen in vertiefter Bearbeitung", "p": 3},
                        {"text": "Kapitel miteinander verknüpft", "p": 2},
                    ],
                    "assigned_artifact": "03_va_hauptarbeit.pdf",
                },
                {
                    "name": "Haupttext Eigenständigkeit",
                    "max": 8,
                    "sub": [
                        {"text": "Arbeit selbständig formuliert", "p": 2},
                        {"text": "Mind. ¾ aus Recherchen vor Ort / eigenen Umfragen / Berichten", "p": 3},
                        {"text": "Persönliche Erfahrungen, Kommentare, Stellungnahmen", "p": 3},
                    ],
                    "assigned_artifact": "03_va_hauptarbeit.pdf",
                },
                {
                    "name": "Bilder und Graphiken",
                    "max": 4,
                    "sub": [
                        {"text": "Sinnvoll und unterstützend", "p": 2},
                        {"text": "Kommentiert oder im Text erwähnt", "p": 1},
                        {"text": "Diversity-bewusst gewählt", "p": 1},
                    ],
                    "assigned_artifact": "03_va_hauptarbeit.pdf",
                },
                {
                    "name": "Quellen",
                    "max": 5,
                    "sub": [
                        {"text": "Angemessene Quellenbasis", "p": 2},
                        {"text": "Vollständig und korrekt aufgeführt", "p": 2},
                        {"text": "Kapitel- und Unterkapitel-Zuordnung", "p": 1},
                    ],
                    "assigned_artifact": "03_va_hauptarbeit.pdf",
                },
                {
                    "name": "Schluss",
                    "max": 4,
                    "sub": [
                        {"text": "Zusammenfassung zu erreichten Zielen (4-5 Sätze)", "p": 1},
                        {"text": "Persönlicher, gut fundierter Kommentar (½ Seite)", "p": 3},
                    ],
                    "assigned_artifact": "03_va_hauptarbeit.pdf",
                },
                {
                    "name": "Sprache",
                    "max": 7,
                    "sub": [
                        {"text": "Wortwahl differenziert, Satzbau korrekt", "p": 4},
                        {"text": "Grammatik und Rechtschreibung korrekt", "p": 2},
                        {"text": "Gender- und diversity-bewusste Sprache", "p": 1},
                    ],
                    "assigned_artifact": "03_va_hauptarbeit.pdf",
                },
            ],
        },
        "C_praesentation": {
            "name": "C Präsentation",
            "max": 40,
            "kriterien": [
                {"name": "Struktur und Inhalt", "max": 20, "sub": [], "assigned_artifact": "19_schlusspraesentation.pptx"},
                {"name": "Nonverbales Verhalten", "max": 5, "sub": [], "assigned_artifact": None},
                {"name": "Verbales Verhalten", "max": 5, "sub": [], "assigned_artifact": None},
                {"name": "Visualisierung", "max": 10, "sub": [], "assigned_artifact": "19_schlusspraesentation.pptx"},
            ],
        },
    },
    "notenskala": [
        [114, 6.0], [102, 5.5], [90, 5.0], [78, 4.5], [66, 4.0],
        [54, 3.5], [42, 3.0], [30, 2.5], [18, 2.0], [6, 1.5], [0, 1.0],
    ],
}


def load_rubric() -> Rubric:
    return Rubric.model_validate(_RUBRIC_JSON)

def save_rubric_json(path: Path = config.OUTPUT_DIR / "rubric.json") -> None:
    r = load_rubric()
    atomic_write_json(path, r.model_dump(mode="json"))

if __name__ == "__main__":
    save_rubric_json()
    print(f"Rubric gespeichert: {config.OUTPUT_DIR / 'rubric.json'}")
```

- [ ] **Step 3: Test grün + Rubric dumpen**

```bash
pytest tests/test_rubric_parser.py -v
python -m scripts.rubric_parser
cat _output/agent/rubric.json | head -20
```

Expected: Tests PASS, JSON wird korrekt geschrieben.

- [ ] **Step 4: Commit**

```bash
git add scripts/rubric_parser.py tests/test_rubric_parser.py
git commit -m "feat: 120-point rubric structure from Wegleitung S. 23-25"
```

---

---

## Milestone 6: Konzept-Agent (Pattern-Setter) (45m · bis 21:05)

Dieser Agent etabliert das **Pattern, dem alle LLM-Subagenten folgen**. Genau durchgehen, die anderen sind dann mechanisch.

### Task 6.1: Subagent-Base-Protocol

**Files:**
- Create: `scripts/subagents/base.py`

- [ ] **Step 1: Base-Modul schreiben**

```python
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
```

- [ ] **Step 2: Commit**

```bash
git add scripts/subagents/base.py
git commit -m "feat: subagent base (claude client, jinja prompts, event emits)"
```

### Task 6.2: Konzept-Prompt-Template

**Files:**
- Create: `scripts/prompts/konzept.j2`

- [ ] **Step 1: Prompt schreiben**

```jinja
Du bist {{ u.schuelerin.vorname }} {{ u.schuelerin.nachname }}, FaGe-Lernende:r im 5. Semester an {{ u.schuelerin.schule }}, Lehrbetrieb {{ u.schuelerin.lehrbetrieb }}.

Schreibe das VA-Konzept zu deiner Vertiefungsarbeit.

Rahmenthema: {{ u.thema.rahmen }}
Dein Titel: {{ u.thema.titel }}
Aspekte/Blickwinkel der Allgemeinbildung: {{ u.thema.aspekte | join(", ") }}
Methoden, die du wählst: {{ u.thema.methoden | join(", ") }}

Pflichtstruktur (Markdown, strikt einhalten):

# VA-Konzept

## 1. Themenbegründung
- Allgemein: Warum ist das Thema relevant? (2-3 Sätze, mit Bezug zum Rahmenthema "{{ u.thema.rahmen }}")
- Persönlich: Warum interessiert es DICH? (2-3 Sätze, als {{ u.schuelerin.vorname }}, mit persönlichem Bezug zum Spitex-Alltag)
- Wissenszuwachs: Was wirst du konkret Neues lernen? (1-2 Sätze)

## 2. Aspekte der Allgemeinbildung
Bezug zu {{ u.thema.aspekte | length }} ABU-Aspekten: {{ u.thema.aspekte | join(", ") }}. Für jeden 2-3 Sätze, was konkret.

## 3. Ziele (3 Stück, je mit Vorgehen)
Formuliere exakt DREI Ziele im Schema:
- **Was** will ich tun? (Inhalt, mit konkretem Verb wie "untersuchen", "analysieren", "ermitteln", "aufzeigen", "darstellen", "vergleichen", "erörtern", "beurteilen")
- **Wie** will ich es tun? (Methode: Interview, Umfrage, Reportage, etc.)
- **Welches Resultat** soll entstehen? (Endprodukt konkret)

Jedes Ziel verweist auf einen der Aspekte. Jedes Ziel ist realisierbar.

## 4. Methoden (mindestens 2)
- Methode 1: {{ u.thema.methoden[0] }} — warum gewählt, wie durchgeführt
- Methode 2: {{ u.thema.methoden[1] }} — warum gewählt, wie durchgeführt

## 5. Zeitplan (8 Wochen)
Tabelle mit 8 Wochen, Spalten: Woche | Datum-Start | Geplante Tätigkeit. Nutze diese Timeline:
{% for w in u.timeline %}
- Woche {{ w.woche }}, {{ w.datum_start }}: {{ w.highlights }}
{% endfor %}

## 6. Disposition (vorläufige Gliederung der VA)
- 1. Einleitung
- 2. [Kapitel zum ersten Ziel]
- 3. [Kapitel zum zweiten Ziel]
- 4. [Kapitel zum dritten Ziel]
- 5. Schlusswort

Stil:
- Schreibe in der ICH-Form als {{ u.schuelerin.vorname }}
- Gender mit Doppelpunkt (Lernende:r, Klient:innen, Fachpersonen)
- Etwas jugendlicher Tonfall, aber fachlich korrekt
- Schreibstil-Marker: {{ u.schuelerin.schreibstil_marker | join("; ") }}

Länge insgesamt: 2-3 A4-Seiten (ca. 700-1000 Wörter).

Gib NUR das Markdown zurück, ohne weitere Meta-Kommentare.
```

- [ ] **Step 2: Commit**

```bash
git add scripts/prompts/konzept.j2
git commit -m "feat: konzept prompt template"
```

### Task 6.3: Konzept-HTML-Template + CSS

**Files:**
- Create: `templates/va_css.css`
- Create: `templates/konzept_html.j2`

- [ ] **Step 1: Master-CSS**

```css
/* templates/va_css.css — Wegleitung-konform: Arial 11, LS 1.5 */
@page {
  size: A4;
  margin: 2.5cm 2cm 2.5cm 2.5cm;
  @bottom-right { content: counter(page); font-family: Arial; font-size: 9pt; color: #666; }
}
html { font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.5; color: #000; }
body { margin: 0; }
h1 { font-size: 18pt; font-weight: bold; margin: 0 0 0.6em 0; page-break-after: avoid; }
h2 { font-size: 14pt; font-weight: bold; margin: 1em 0 0.4em 0; page-break-after: avoid; }
h3 { font-size: 12pt; font-weight: bold; margin: 0.8em 0 0.3em 0; page-break-after: avoid; }
p { margin: 0 0 0.5em 0; text-align: justify; hyphens: auto; }
ul, ol { margin: 0 0 0.5em 1.5em; padding: 0; }
li { margin-bottom: 0.2em; }
table { border-collapse: collapse; margin: 0.5em 0; width: 100%; }
th, td { border: 1px solid #999; padding: 4pt 6pt; text-align: left; vertical-align: top; }
th { background: #e8e8e8; font-weight: bold; }
img { max-width: 100%; height: auto; page-break-inside: avoid; }
.page-break { page-break-before: always; }
.footnote { font-size: 9pt; color: #555; border-top: 1px solid #999; padding-top: 4pt; margin-top: 8pt; }
.quote { margin: 0.5em 1.5em; padding: 0 0.5em; border-left: 3px solid #999; font-style: italic; }
.caption { font-size: 9pt; color: #555; text-align: center; margin-top: 4pt; }
```

- [ ] **Step 2: Konzept-HTML-Template**

```jinja
{# templates/konzept_html.j2 — wird von pdf_render aufgerufen #}
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>VA-Konzept — {{ u.thema.titel }}</title>
<style>{{ css }}</style>
</head>
<body>
{{ body_html | safe }}
<div class="footnote">
Autor:in: {{ u.schuelerin.vorname }} {{ u.schuelerin.nachname }} · Klasse {{ u.schuelerin.klasse }} · {{ u.schuelerin.schule }} · Lehrperson: {{ u.schuelerin.lehrperson }}
</div>
</body>
</html>
```

- [ ] **Step 3: Commit**

```bash
git add templates/va_css.css templates/konzept_html.j2
git commit -m "feat: master CSS (Arial 11, LS 1.5) + konzept HTML template"
```

### Task 6.4: pdf_render.py

**Files:**
- Create: `scripts/media/pdf_render.py`
- Create: `tests/test_pdf_render.py`

- [ ] **Step 1: Test**

```python
# tests/test_pdf_render.py
import pytest
from pathlib import Path
from scripts.media.pdf_render import render_markdown_to_pdf

def test_render_simple(tmp_path):
    md = "# Test\n\nEin kleiner Absatz."
    out = tmp_path / "out.pdf"
    meta = {"u": None, "title": "Test"}
    render_markdown_to_pdf(md, out, template_name="konzept_html.j2", extra_ctx={"u": _sample_u()})
    assert out.exists()
    assert out.stat().st_size > 1000  # mind. 1 KB

def _sample_u():
    from scripts.coherence import Universe
    return Universe.sample()
```

- [ ] **Step 2: pdf_render.py implementieren**

```python
"""HTML/Markdown → PDF via WeasyPrint."""
from __future__ import annotations
from pathlib import Path
import markdown as md_lib
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML, CSS

from scripts import config

_jinja = Environment(
    loader=FileSystemLoader(str(config.TEMPLATES_DIR)),
    autoescape=select_autoescape(["html"]),
)

def load_css() -> str:
    return (config.TEMPLATES_DIR / "va_css.css").read_text(encoding="utf-8")

def render_markdown_to_pdf(markdown: str, out_path: Path, template_name: str = "konzept_html.j2", extra_ctx: dict | None = None) -> None:
    body_html = md_lib.markdown(markdown, extensions=["tables", "fenced_code", "toc"])
    tpl = _jinja.get_template(template_name)
    html_str = tpl.render(
        body_html=body_html,
        css=load_css(),
        **(extra_ctx or {}),
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html_str, base_url=str(config.PROJECT_ROOT)).write_pdf(str(out_path))

def render_html_to_pdf(html_str: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html_str, base_url=str(config.PROJECT_ROOT)).write_pdf(str(out_path))
```

Add `markdown` dependency:

```bash
pip install markdown>=3.6
# in pyproject.toml dependencies: "markdown>=3.6"
```

Add to `pyproject.toml` dependencies: `"markdown>=3.6",`

- [ ] **Step 3: Test grün**

```bash
pytest tests/test_pdf_render.py -v
```

Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add scripts/media/pdf_render.py tests/test_pdf_render.py pyproject.toml
git commit -m "feat: markdown → PDF via WeasyPrint"
```

### Task 6.5: Konzept-Subagent

**Files:**
- Create: `scripts/subagents/konzept.py`

- [ ] **Step 1: Subagent-Datei schreiben**

```python
"""Konzept-Subagent. Pattern-Setter für alle anderen LLM-Subagenten."""
from __future__ import annotations
import time
from pathlib import Path

from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import (
    SubagentResult, claude_opus_complete, render_prompt,
    emit_start, emit_done, emit_warn,
)
from scripts.media.pdf_render import render_markdown_to_pdf
from scripts.utils import log

PHASE = 3
NAME = "konzept"

SYSTEM = "Du schreibst Texte für eine Schweizer FaGe-Vertiefungsarbeit. Du schreibst in der ICH-Form aus Sicht der Lernenden. Kein Meta-Kommentar, kein 'ich würde schreiben'."

async def run(u: Universe) -> SubagentResult:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()
    user_prompt = render_prompt("konzept.j2", u=u)
    markdown = await claude_opus_complete(system=SYSTEM, user=user_prompt, max_tokens=4096, stream=True, phase=PHASE, task_name=NAME)
    out = config.ARTIFACTS_DIR / "02_konzept.pdf"
    render_markdown_to_pdf(markdown, out, template_name="konzept_html.j2", extra_ctx={"u": u})
    # auch markdown als Quelle speichern (für Self-Check)
    (config.ARTIFACTS_DIR / "02_konzept.md").write_text(markdown, encoding="utf-8")
    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"{out.name} ({out.stat().st_size // 1024} KB)")
    log.info(f"[{NAME}] Konzept fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=out, duration_s=duration)
```

- [ ] **Step 2: Isolierter Dev-Test**

Create: `scripts/dev_test_konzept.py`

```python
"""Einmaliger Test: Konzept-Agent alleine ausführen."""
import asyncio
from scripts.coherence import Universe
from scripts.subagents import konzept

async def main():
    u = Universe.sample()
    result = await konzept.run(u)
    print(f"✅ {result.output_path} in {result.duration_s:.1f}s")

if __name__ == "__main__":
    asyncio.run(main())
```

```bash
python scripts/dev_test_konzept.py
open _output/agent/artifacts/02_konzept.pdf
```

Expected: PDF öffnet sich, enthält ein vollständiges Konzept mit 6 Sektionen.

- [ ] **Step 3: Qualitätskontrolle**

Prüfe manuell:
- Alle 6 Sektionen da (Themenbegründung, Aspekte, Ziele, Methoden, Zeitplan, Disposition)
- 3 Ziele explizit durchnummeriert
- 2 Methoden begründet
- 8-Wochen-Zeitplan als Tabelle
- Arial 11, Zeilenabstand 1.5
- Name "Luca Brunner" im Footer

Wenn schlecht: Prompt iterieren.

- [ ] **Step 4: Commit**

```bash
git add scripts/subagents/konzept.py scripts/dev_test_konzept.py
git commit -m "feat: Konzept-Subagent (9/9-point pattern setter)"
```

---

## Milestone 7: Literatur-Agent (45m · bis 21:50)

### Task 7.1: HTTP-Tools für Quellen-Recherche

**Files:**
- Create: `scripts/tools/openalex.py`
- Create: `scripts/tools/google_books.py`
- Create: `scripts/tools/pubmed.py`
- Create: `scripts/tools/srf_fetch.py`

- [ ] **Step 1: openalex.py**

```python
"""OpenAlex-Client für wissenschaftliche Publikationen."""
from __future__ import annotations
import httpx
from typing import Any

BASE = "https://api.openalex.org"

async def search_works(query: str, year_from: int = 2018, per_page: int = 10) -> list[dict[str, Any]]:
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(
            f"{BASE}/works",
            params={
                "search": query,
                "filter": f"from_publication_date:{year_from}-01-01,has_abstract:true,language:de|en",
                "per-page": per_page,
                "mailto": "picts-demo@example.ch",  # OpenAlex empfiehlt
            },
        )
        r.raise_for_status()
        data = r.json()
    results = []
    for w in data.get("results", []):
        results.append({
            "title": w.get("title") or "",
            "authors": [a["author"]["display_name"] for a in w.get("authorships", [])[:5] if a.get("author")],
            "year": w.get("publication_year"),
            "doi": w.get("doi"),
            "venue": (w.get("primary_location") or {}).get("source", {}).get("display_name") if w.get("primary_location") else None,
            "abstract": _reconstruct_abstract(w.get("abstract_inverted_index")),
            "open_access_url": (w.get("open_access") or {}).get("oa_url"),
        })
    return results

def _reconstruct_abstract(inverted_index: dict | None) -> str:
    if not inverted_index:
        return ""
    pos_to_word: dict[int, str] = {}
    for word, positions in inverted_index.items():
        for p in positions:
            pos_to_word[p] = word
    return " ".join(pos_to_word[i] for i in sorted(pos_to_word))
```

- [ ] **Step 2: google_books.py**

```python
"""Google Books API — echte Bücher mit ISBN & Snippets."""
from __future__ import annotations
import httpx

BASE = "https://www.googleapis.com/books/v1/volumes"

async def search_books(query: str, max_results: int = 8, lang: str = "de") -> list[dict]:
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(BASE, params={
            "q": query,
            "maxResults": max_results,
            "langRestrict": lang,
            "printType": "books",
        })
        r.raise_for_status()
        data = r.json()
    out = []
    for item in data.get("items", []):
        info = item.get("volumeInfo", {})
        ids = {x["type"]: x["identifier"] for x in info.get("industryIdentifiers", [])}
        out.append({
            "title": info.get("title"),
            "authors": info.get("authors", []),
            "publisher": info.get("publisher"),
            "year": (info.get("publishedDate") or "")[:4],
            "isbn_13": ids.get("ISBN_13"),
            "isbn_10": ids.get("ISBN_10"),
            "description": info.get("description"),
            "preview_link": info.get("previewLink"),
            "info_link": info.get("infoLink"),
            "snippet": (item.get("searchInfo") or {}).get("textSnippet"),
        })
    return out
```

- [ ] **Step 3: pubmed.py**

```python
"""PubMed E-utilities — biomedizinische Publikationen."""
from __future__ import annotations
import httpx

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

async def search_pubmed(query: str, max_results: int = 8) -> list[dict]:
    async with httpx.AsyncClient(timeout=15) as client:
        s = await client.get(f"{BASE}/esearch.fcgi", params={
            "db": "pubmed", "term": query, "retmode": "json", "retmax": max_results, "sort": "relevance",
        })
        s.raise_for_status()
        ids = s.json().get("esearchresult", {}).get("idlist", [])
        if not ids:
            return []
        sum_r = await client.get(f"{BASE}/esummary.fcgi", params={
            "db": "pubmed", "id": ",".join(ids), "retmode": "json",
        })
        sum_r.raise_for_status()
        result = sum_r.json().get("result", {})
    out = []
    for pid in ids:
        doc = result.get(pid, {})
        out.append({
            "pmid": pid,
            "title": doc.get("title"),
            "authors": [a.get("name") for a in doc.get("authors", [])[:5]],
            "journal": doc.get("fulljournalname"),
            "year": (doc.get("pubdate") or "")[:4],
            "doi": next((x["value"] for x in doc.get("articleids", []) if x.get("idtype") == "doi"), None),
        })
    return out
```

- [ ] **Step 4: srf_fetch.py (minimal)**

```python
"""SRF-Artikel holen (nur für Whitelist-URLs)."""
from __future__ import annotations
import httpx
from bs4 import BeautifulSoup

ALLOWED_HOSTS = {"www.srf.ch", "srf.ch"}

async def fetch_srf_article(url: str) -> dict:
    from urllib.parse import urlparse
    host = urlparse(url).hostname
    if host not in ALLOWED_HOSTS:
        raise ValueError(f"Host {host} nicht in Whitelist")
    async with httpx.AsyncClient(timeout=15, headers={"User-Agent": "Mozilla/5.0"}) as client:
        r = await client.get(url)
        r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.find("h1").get_text(strip=True) if soup.find("h1") else ""
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")][:8]
    return {"url": url, "title": title, "paragraphs": paragraphs}
```

Add `beautifulsoup4` to pyproject.toml.

- [ ] **Step 5: Dev-Test**

```bash
python -c "
import asyncio
from scripts.tools.google_books import search_books
async def m(): print(await search_books('Einsamkeit im Alter Pflege', 3))
asyncio.run(m())
"
```

Expected: JSON-Output mit 3 Büchern inkl. ISBN.

- [ ] **Step 6: Commit**

```bash
git add scripts/tools/ pyproject.toml
git commit -m "feat: literature research tools (OpenAlex, Google Books, PubMed, SRF)"
```

### Task 7.2: Literatur-Agent

**Files:**
- Create: `scripts/subagents/literatur.py`
- Create: `scripts/prompts/literatur_search_plan.j2`

- [ ] **Step 1: Search-Plan-Prompt**

```jinja
{# scripts/prompts/literatur_search_plan.j2 #}
Du planst die Literaturrecherche für eine Vertiefungsarbeit.

Thema: {{ u.thema.titel }}
Rahmen: {{ u.thema.rahmen }}
Aspekte: {{ u.thema.aspekte | join(", ") }}

Gib EXAKT folgendes JSON zurück (keine Markdown-Fences, nur JSON):
{
  "google_books_queries": ["...", "...", "..."],     // 3 Suchbegriffe (Deutsch, CH-Fokus)
  "openalex_queries": ["...", "..."],                 // 2 Suchbegriffe (Englisch, akademisch)
  "pubmed_queries": ["..."],                          // 1 Suchbegriff (wenn Gesundheitsthema, sonst leer)
  "srf_urls": ["https://www.srf.ch/..."]              // 1-2 reale SRF-URLs, die zum Thema passen, aus deinem Wissen
}

Qualitätsregeln:
- Mindestens eine Query mit "Schweiz" oder "Zürich"
- Queries sind konkret genug um Volltreffer zu geben
- SRF-URLs sind reale Pfade, die du aus dem Training kennst (kein Halluzinieren!)
```

- [ ] **Step 2: Literatur-Subagent**

```python
"""Literatur-Agent: plant Suchen, ruft Tools, paraphrasiert Snippets."""
from __future__ import annotations
import asyncio
import json
import time

from scripts.coherence import Universe, Quelle
from scripts.subagents.base import (
    SubagentResult, claude_sonnet_complete, render_prompt,
    emit_start, emit_done, emit_warn,
)
from scripts.tools.google_books import search_books
from scripts.tools.openalex import search_works
from scripts.tools.pubmed import search_pubmed
from scripts.tools.srf_fetch import fetch_srf_article
from scripts.utils import log

PHASE = 4
NAME = "literatur"
SYSTEM = "Du planst Literatursuchen. Du antwortest immer mit gültigem JSON und nichts anderem."


async def run(u: Universe) -> tuple[SubagentResult, list[Quelle]]:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()
    plan_user = render_prompt("literatur_search_plan.j2", u=u)
    plan_json_str = await claude_sonnet_complete(system=SYSTEM, user=plan_user, max_tokens=800)
    plan = _extract_json(plan_json_str)

    gb_tasks = [search_books(q, 4) for q in plan.get("google_books_queries", [])]
    oa_tasks = [search_works(q, 2018, 4) for q in plan.get("openalex_queries", [])]
    pm_tasks = [search_pubmed(q, 4) for q in plan.get("pubmed_queries", [])]
    srf_tasks = [fetch_srf_article(url) for url in plan.get("srf_urls", [])]

    all_results = await asyncio.gather(*gb_tasks, *oa_tasks, *pm_tasks, *srf_tasks, return_exceptions=True)

    gb_results = all_results[:len(gb_tasks)]
    oa_results = all_results[len(gb_tasks):len(gb_tasks)+len(oa_tasks)]
    pm_results = all_results[len(gb_tasks)+len(oa_tasks):len(gb_tasks)+len(oa_tasks)+len(pm_tasks)]
    srf_results = all_results[len(gb_tasks)+len(oa_tasks)+len(pm_tasks):]

    quellen: list[Quelle] = []
    for batch in gb_results:
        if isinstance(batch, Exception): continue
        for b in batch[:2]:
            if not b.get("title") or not (b.get("isbn_13") or b.get("isbn_10")):
                continue
            quellen.append(Quelle(
                typ="buch",
                autor=", ".join(b.get("authors") or []) or "Unbekannt",
                titel=b["title"],
                jahr=int(b["year"]) if b.get("year") and b["year"].isdigit() else None,
                verlag=b.get("publisher"),
                isbn=b.get("isbn_13") or b.get("isbn_10"),
                url=b.get("info_link"),
                snippet=b.get("snippet") or (b.get("description") or "")[:500],
                real_verified=True,
                api_source="google_books",
            ))
    for batch in oa_results:
        if isinstance(batch, Exception): continue
        for w in batch[:2]:
            if not w.get("title"): continue
            quellen.append(Quelle(
                typ="fachartikel",
                autor=", ".join(w.get("authors") or []) or "Unbekannt",
                titel=w["title"],
                jahr=w.get("year"),
                verlag=w.get("venue"),
                doi=w.get("doi"),
                url=w.get("open_access_url"),
                snippet=(w.get("abstract") or "")[:800],
                real_verified=True,
                api_source="openalex",
            ))
    for batch in pm_results:
        if isinstance(batch, Exception): continue
        for p in batch[:2]:
            quellen.append(Quelle(
                typ="fachartikel",
                autor=", ".join(p.get("authors") or []) or "Unbekannt",
                titel=p["title"] or "",
                jahr=int(p["year"]) if p.get("year") and p["year"].isdigit() else None,
                verlag=p.get("journal"),
                doi=p.get("doi"),
                snippet="",
                real_verified=True,
                api_source="pubmed",
            ))
    for art in srf_results:
        if isinstance(art, Exception): continue
        quellen.append(Quelle(
            typ="internet",
            autor="SRF Redaktion",
            titel=art.get("title") or "SRF-Beitrag",
            url=art["url"],
            snippet=" ".join(art.get("paragraphs", []))[:800],
            real_verified=True,
            api_source="srf",
        ))

    # Mindestens 8 Quellen garantieren
    if len(quellen) < 8:
        await emit_warn(NAME, PHASE, f"Nur {len(quellen)} Quellen gefunden, Minimum 8")

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"{len(quellen)} Quellen")
    log.info(f"[{NAME}] {len(quellen)} Quellen in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=None, duration_s=duration), quellen


def _extract_json(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(raw)
```

- [ ] **Step 3: Dev-Test**

Create: `scripts/dev_test_literatur.py`

```python
import asyncio
from scripts.coherence import Universe
from scripts.subagents import literatur

async def main():
    u = Universe.sample()
    result, quellen = await literatur.run(u)
    print(f"✅ {len(quellen)} Quellen in {result.duration_s:.1f}s")
    for q in quellen:
        print(f"  [{q.typ}] {q.autor} — {q.titel} ({q.jahr})")

asyncio.run(main())
```

```bash
python scripts/dev_test_literatur.py
```

Expected: ≥ 8 Quellen, davon mind. 2 mit ISBN (Bücher) und mind. 2 Fachartikel.

- [ ] **Step 4: Commit**

```bash
git add scripts/subagents/literatur.py scripts/prompts/literatur_search_plan.j2 scripts/dev_test_literatur.py
git commit -m "feat: Literatur-Subagent mit 4 parallelen Quellen-Tools"
```

---

## Milestone 8: Interview + Audio (45m · bis 22:35)

### Task 8.1: Interview-Prompts + Subagent

**Files:**
- Create: `scripts/prompts/interview_leitfaden.j2`
- Create: `scripts/prompts/interview_transkript.j2`
- Create: `scripts/subagents/interview.py`

- [ ] **Step 1: Leitfaden-Prompt**

```jinja
{# interview_leitfaden.j2 #}
Erstelle einen Frageleitfaden für ein Fachinterview.

Kontext:
- Interviewperson: {{ u.interviewperson.name_anzeige }} ({{ u.interviewperson.funktion }})
- Thema: {{ u.thema.titel }}
- Durchführung: {{ u.interviewperson.interview_termin }}, ca. 40 Min

Output (reines Markdown, keine JSON-Fences):

# Frageleitfaden Interview {{ u.interviewperson.name_anzeige }}

## 1. Einstieg
- Begrüssung, Dank
- Einverständnis für Tonaufnahme bestätigen
- Kurze Vorstellung Luca Brunner + VA-Ziel

## 2. Fragen zum Hintergrund der Interviewperson (2 Fragen)
...

## 3. Fachfragen (6 Fragen, offen formuliert)
Zu den Aspekten: {{ u.thema.aspekte | join(", ") }}
...

## 4. Persönliche Einschätzungen (3 Fragen)
...

## 5. Abschluss (1 Frage)
- Was geben Sie FaGe-Lernenden mit auf den Weg?

Länge: 12 Fragen total, davon mindestens 8 offene W-Fragen.
```

- [ ] **Step 2: Transkript-Prompt**

```jinja
{# interview_transkript.j2 #}
Erstelle ein realistisches Interview-Transkript.

Setting: {{ u.interviewperson.interview_termin }}, im Büro von {{ u.interviewperson.name_anzeige }} an der ZHAW.
Interviewer: {{ u.schuelerin.vorname }} {{ u.schuelerin.nachname }} (FaGe-Lernende:r, 19).
Interviewte: {{ u.interviewperson.name_anzeige }} ({{ u.interviewperson.funktion }}, {{ u.interviewperson.alter }}).

Der Leitfaden:
{{ leitfaden }}

Regeln für Realismus:
- Die Antworten sind ~3-6 Sätze, manchmal länger bei Kernpunkten
- {{ u.schuelerin.vorname }} stellt genau die Fragen des Leitfadens — aber manchmal stottert er kurz ("ähm, also…", "ich wollte fragen…")
- Dr. Weber antwortet professionell, referenziert gelegentlich Studien oder ihre eigene Erfahrung
- 2-3 Mal formuliert Dr. Weber eine Frage von Luca um, weil sie präziser sein möchte
- 1× lange Pause (im Transkript als "[kurze Pause]" markiert)
- 1× persönliche Anekdote von Dr. Weber (ca. 30 Sekunden)
- 1× Luca bittet um Wiederholung
- 1× Hintergrundgeräusch ("[Kaffeetasse wird abgestellt]")
- Schweizer Hochdeutsch mit leicht gesprochener Note bei Luca, formell bei Dr. Weber
- Am Schluss: Dank, Zusage Luca darf zitieren

Format:

# Interview-Transkript: {{ u.interviewperson.name_anzeige }}

**Datum:** {{ u.interviewperson.interview_termin }}
**Ort:** ZHAW Winterthur, Büro Dr. Weber
**Dauer:** 42 Minuten
**Aufnahme:** Tonaufnahme (mit Einverständnis)
**Teilnehmende:** {{ u.schuelerin.vorname }} {{ u.schuelerin.nachname }} (Interviewer), {{ u.interviewperson.name_anzeige }} (Interviewte)

---

**Luca:** ...

**Dr. Weber:** ...

**Luca:** ...

[... fortsetzen für 12 Fragen + Antworten ...]

---

**Ende Transkript.**

Zielumfang: ~2500 Wörter.
```

- [ ] **Step 3: Interview-Subagent**

```python
"""Interview-Agent: Leitfaden + Transkript."""
from __future__ import annotations
import time
from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import (
    SubagentResult, claude_opus_complete, render_prompt,
    emit_start, emit_done,
)
from scripts.media.pdf_render import render_markdown_to_pdf
from scripts.utils import log

PHASE = 4
NAME = "interview"

SYSTEM = "Du erstellst realistische Interview-Inhalte. Keine Meta-Kommentare."

async def run(u: Universe) -> tuple[SubagentResult, str]:
    """Returns (result, transkript_markdown) — Audio-Agent braucht das Transkript."""
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    leitfaden_md = await claude_opus_complete(
        system=SYSTEM,
        user=render_prompt("interview_leitfaden.j2", u=u),
        max_tokens=2048,
    )
    transkript_md = await claude_opus_complete(
        system=SYSTEM,
        user=render_prompt("interview_transkript.j2", u=u, leitfaden=leitfaden_md),
        max_tokens=6000,
        stream=True, phase=PHASE, task_name=NAME,
    )

    leit_pdf = config.ARTIFACTS_DIR / "12a_interview_leitfaden.pdf"
    trans_pdf = config.ARTIFACTS_DIR / "12_interview_transkript.pdf"
    render_markdown_to_pdf(leitfaden_md, leit_pdf, template_name="konzept_html.j2", extra_ctx={"u": u})
    render_markdown_to_pdf(transkript_md, trans_pdf, template_name="konzept_html.j2", extra_ctx={"u": u})
    (config.ARTIFACTS_DIR / "12_interview_transkript.md").write_text(transkript_md, encoding="utf-8")

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"{trans_pdf.name}")
    log.info(f"[{NAME}] Transkript fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=trans_pdf, duration_s=duration), transkript_md
```

- [ ] **Step 4: Dev-Test**

```bash
python -c "
import asyncio
from scripts.coherence import Universe
from scripts.subagents import interview
async def m():
    u = Universe.sample()
    r, md = await interview.run(u)
    print(f'OK {r.output_path} {r.duration_s:.1f}s {len(md)} Zeichen')
asyncio.run(m())
"
open _output/agent/artifacts/12_interview_transkript.pdf
```

Expected: PDF mit ~6-8 Seiten Transkript, realistische Dialogstruktur.

- [ ] **Step 5: Commit**

```bash
git add scripts/subagents/interview.py scripts/prompts/interview_*.j2
git commit -m "feat: Interview-Subagent (Leitfaden + Transkript)"
```

### Task 8.2: Audio-Agent (TTS für Interview)

**Files:**
- Create: `scripts/media/tts_elevenlabs.py`
- Create: `scripts/subagents/audio.py`

- [ ] **Step 1: TTS-Modul**

```python
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
```

- [ ] **Step 2: Audio-Subagent**

```python
"""Audio-Agent: Transkript → MP3 mit zwei Stimmen."""
from __future__ import annotations
import re
import time
from pathlib import Path
from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import SubagentResult, emit_start, emit_done, emit_warn
from scripts.media.tts_elevenlabs import synth_turn, concat_mp3s
from scripts.utils import log

PHASE = 4
NAME = "audio"

# Regex: **Luca:** oder **Dr. Weber:** am Zeilenanfang
_SPEAKER_RE = re.compile(r"^\*\*(Luca|Dr\. Weber|Dr\.\s?Andrea Weber)[:]\*\*\s*(.*)$", re.MULTILINE)


def parse_turns(transkript_md: str) -> list[tuple[str, str]]:
    """Returns list of (speaker, text)."""
    turns: list[tuple[str, str]] = []
    for m in _SPEAKER_RE.finditer(transkript_md):
        speaker = "luca" if m.group(1).lower().startswith("luca") else "weber"
        text = m.group(2).strip()
        # Strip marker wie [kurze Pause] etc.
        text = re.sub(r"\[[^\]]+\]", "", text).strip()
        if text:
            turns.append((speaker, text))
    return turns


async def run(u: Universe, transkript_md: str) -> SubagentResult:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()
    turns = parse_turns(transkript_md)
    if not turns:
        await emit_warn(NAME, PHASE, "Keine Turns im Transkript gefunden!")
        return SubagentResult(name=NAME, output_path=None, duration_s=0)

    tmp_dir = config.OUTPUT_DIR / "audio_tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    parts: list[Path] = []
    voice_luca = u.schuelerin.voice_id_elevenlabs
    voice_weber = u.interviewperson.tts_voice_id

    # Budget: max 60 Turns, 8 Min Audio. Bei mehr: kürzen.
    for i, (spk, text) in enumerate(turns[:60]):
        vid = voice_luca if spk == "luca" else voice_weber
        part = tmp_dir / f"t{i:03d}_{spk}.mp3"
        synth_turn(vid, text, part)
        parts.append(part)

    out = config.ARTIFACTS_DIR / "13_interview_audio.mp3"
    concat_mp3s(parts, out, pause_ms=400)
    # Cleanup tmp
    for p in parts:
        p.unlink(missing_ok=True)

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"{out.stat().st_size // 1024} KB")
    log.info(f"[{NAME}] Audio fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=out, duration_s=duration)
```

- [ ] **Step 3: Dev-Test**

```bash
python -c "
import asyncio
from pathlib import Path
from scripts.coherence import Universe
from scripts.subagents import audio
async def m():
    u = Universe.sample()
    md = Path('_output/agent/artifacts/12_interview_transkript.md').read_text()
    r = await audio.run(u, md)
    print(r)
asyncio.run(m())
"
open _output/agent/artifacts/13_interview_audio.mp3
```

Expected: MP3 spielt ab, ~6-8 Min, zwei unterscheidbare Stimmen.

- [ ] **Step 4: Commit**

```bash
git add scripts/media/tts_elevenlabs.py scripts/subagents/audio.py
git commit -m "feat: Audio-Subagent via ElevenLabs TTS + ffmpeg concat"
```

---

## Milestone 9: Video-Agent (Runway + Hedra) (45m · bis 23:20)

### Task 9.1: Runway B-Roll

**Files:**
- Create: `scripts/media/video_runway.py`

- [ ] **Step 1: Runway-Client**

```python
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
```

### Task 9.2: Hedra Lip-Sync

**Files:**
- Create: `scripts/media/video_hedra.py`

- [ ] **Step 1: Hedra-Client**

```python
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
```

### Task 9.3: Video-Subagent (orchestriert beide)

**Files:**
- Create: `scripts/subagents/video.py`

- [ ] **Step 1: Subagent**

```python
"""Video-Subagent: B-Roll (Runway) + Lip-Sync (Hedra), parallel."""
from __future__ import annotations
import asyncio
import time
from pathlib import Path
from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import SubagentResult, emit_start, emit_done, emit_warn
from scripts.media.video_runway import generate_broll
from scripts.media.video_hedra import generate_lipsync
from scripts.utils import log

PHASE = 4
NAME = "video"

async def run(u: Universe, weber_image: Path, interview_audio: Path) -> SubagentResult:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    broll_out = config.ARTIFACTS_DIR / "17_video_broll.mp4"
    lipsync_out = config.ARTIFACTS_DIR / "14_interview_video_lipsync.mp4"

    broll_prompt = f"Warme Spitex-Szene, Pflegefachperson besucht ältere alleinlebende Frau zuhause, Tageslicht durchs Fenster, cinematic dokumentarisch, ruhige Kamerafahrt, 35mm Film look."
    results = await asyncio.gather(
        _safe(generate_broll, NAME, "broll", broll_prompt, broll_out, 6),
        _safe(generate_lipsync, NAME, "lipsync", weber_image, interview_audio, lipsync_out, 20),
        return_exceptions=False,
    )
    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"broll={results[0] is not None}, lipsync={results[1] is not None}")
    log.info(f"[{NAME}] Video fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=lipsync_out, duration_s=duration)

async def _safe(fn, parent_name, subname, *args):
    try:
        return await fn(*args)
    except Exception as e:
        await emit_warn(parent_name, PHASE, f"{subname} failed: {e}")
        return None
```

- [ ] **Step 2: Commit**

```bash
git add scripts/media/video_runway.py scripts/media/video_hedra.py scripts/subagents/video.py
git commit -m "feat: Video-Subagent (Runway B-Roll + Hedra Lip-Sync)"
```

**Hinweis:** Video-APIs sind heikel — teste sie separat, bevor du sie in Orchestrator einbaust. Wenn zu flaky, Fallback: statt Video ein animiertes Standbild mit Ken-Burns-Effekt via ffmpeg.

---

## Milestone 10: Foto-Agent (FLUX) (20m · bis 23:40)

### Task 10.1: FLUX via fal-client

**Files:**
- Create: `scripts/media/image_flux.py`
- Create: `scripts/subagents/foto.py`

- [ ] **Step 1: image_flux.py**

```python
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
```

- [ ] **Step 2: Foto-Subagent**

```python
"""Foto-Subagent: 5 Bilder (Dr. Weber, Luca+Weber, Spitex-Szene, Einsamkeit-Symbol, Umfrage-Zettel)."""
from __future__ import annotations
import asyncio
import time
from pathlib import Path
from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import SubagentResult, emit_start, emit_done
from scripts.media.image_flux import generate_image
from scripts.utils import log

PHASE = 4
NAME = "foto"

async def run(u: Universe) -> tuple[SubagentResult, dict[str, Path]]:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    targets = {
        "weber_portrait": (u.interviewperson.foto_prompt, "portrait_4_3"),
        "luca_weber": (f"Zwei Personen in einem Büro, Frau ca. 50 mit Brille und graumeliertem Haar, junger Mann ca. 19 Jahre daneben, beide lächeln in die Kamera, natürliches Licht, professionelle Bürostimmung", "landscape_4_3"),
        "spitex_szene": ("Pflegefachperson zu Besuch bei älterer Klientin zuhause, ruhige Wohnzimmer-Atmosphäre, Tageslicht, dokumentarische Warmheit", "landscape_4_3"),
        "einsamkeit_symbol": ("Einzelne ältere Person am Fenster, gedämpftes Tageslicht, kontemplativ, schwarzweiss, poetisch, konzeptuell", "portrait_4_3"),
        "umfrage_zettel": ("Papierfragebogen auf Holztisch, Kugelschreiber daneben, Kaffeetasse im Hintergrund, Top-Down-Shot, realistisch", "square"),
    }
    tasks = [generate_image(p, config.ARTIFACTS_DIR / f"foto_{k}.png", a) for k, (p, a) in targets.items()]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    paths = {}
    for k, r in zip(targets.keys(), results):
        if isinstance(r, Path):
            paths[k] = r

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"{len(paths)}/5 Bilder")
    log.info(f"[{NAME}] Fotos fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=None, duration_s=duration), paths
```

- [ ] **Step 3: Commit**

```bash
git add scripts/media/image_flux.py scripts/subagents/foto.py
git commit -m "feat: Foto-Subagent (5× FLUX 1.2 Pro)"
```

---

---

## Milestone 11: Umfrage-Agent (30m · bis 00:10)

### Task 11.1: Umfrage-Prompts

**Files:**
- Create: `scripts/prompts/umfrage_fragebogen.j2`
- Create: `scripts/prompts/umfrage_antworten.j2`

- [ ] **Step 1: Fragebogen-Prompt**

```jinja
{# umfrage_fragebogen.j2 #}
Erstelle einen Umfrage-Fragebogen zum Thema "{{ u.thema.titel }}".

Zielgruppe: {{ u.umfrage.plattform }}, gemischt: Spitex-FaGe, Klient:innen (ab 65), Angehörige.
Rücklauf-Zielgrösse: {{ u.umfrage.n_ruecklauf }} Personen.

Gib reines JSON zurück (keine Fences):
{
  "titel": "...",
  "einleitung": "Dank-Text mit Zweck-Erklärung, ca. 4 Sätze",
  "fragen": [
    {"nr": 1, "typ": "single_choice", "frage": "...", "optionen": ["...", "..."]},
    {"nr": 2, "typ": "multi_choice", "frage": "...", "optionen": [...]},
    {"nr": 3, "typ": "likert_5", "frage": "...", "optionen": ["Trifft gar nicht zu", "Trifft eher nicht zu", "Teils-teils", "Trifft eher zu", "Trifft voll zu"]},
    {"nr": 4, "typ": "open_short", "frage": "..."}
  ]
}

Regeln:
- Exakt 14 Fragen
- Davon 2 Demografie (Alter, Rolle: FaGe/Klient:in/Angehörige), 10 Inhalt, 2 offen
- Mindestens 3 Likert-5-Fragen
- Konsistent mit Aspekten {{ u.thema.aspekte | join(", ") }}
```

- [ ] **Step 2: Antworten-Prompt**

```jinja
{# umfrage_antworten.j2 #}
Erstelle {{ u.umfrage.n_ruecklauf }} realistische Antwort-Datensätze als CSV.

Fragebogen (JSON):
{{ fragebogen_json }}

Spalten:
- id (1..{{ u.umfrage.n_ruecklauf }})
- alter_gruppe ("18-30", "31-50", "51-70", "71+")
- rolle ("Spitex-FaGe", "Klient:in", "Angehörige:r")
- geschlecht ("weiblich", "männlich", "divers")
- f1 bis f14 (Antwortwerte)

Demografie-Verteilung:
- Alter: 18-30=8, 31-50=14, 51-70=18, 71+=12
- Rolle: Spitex-FaGe=18, Klient:in=28, Angehörige:r=6
- Geschlecht: w=38, m=13, d=1

Konsistenz-Regeln:
- Likert-Antworten plausibel (wer "fühle mich oft einsam" = 5 ankreuzt, gibt bei "soziale Kontakte pro Woche" eher niedrige Zahlen an)
- ~5 % Missing Values (einzelne Zellen leer lassen)
- Bei offenen Fragen: 12 der 52 geben eine kurze Text-Antwort (2-8 Wörter), Rest leer. Antworten auf Schweizer Hochdeutsch, natürliche Sätze, teils mit kleinen Fehlern.

Gib NUR CSV zurück, mit Header-Zeile. Komma-separiert. UTF-8.
```

- [ ] **Step 3: Commit**

```bash
git add scripts/prompts/umfrage_fragebogen.j2 scripts/prompts/umfrage_antworten.j2
git commit -m "feat: umfrage prompt templates"
```

### Task 11.2: Umfrage-Subagent + Plots

**Files:**
- Create: `scripts/subagents/umfrage.py`

- [ ] **Step 1: Subagent**

```python
"""Umfrage-Agent: Fragebogen, synthetische Antworten, Plots, Auswertungstext."""
from __future__ import annotations
import io
import json
import time
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import (
    SubagentResult, claude_opus_complete, claude_sonnet_complete, render_prompt,
    emit_start, emit_done, emit_warn,
)
from scripts.media.pdf_render import render_markdown_to_pdf
from scripts.utils import log

PHASE = 4
NAME = "umfrage"
SYSTEM_JSON = "Du antwortest immer mit reinem JSON, keine Markdown-Fences."
SYSTEM_CSV = "Du antwortest immer mit reinem CSV, kein Kommentar davor oder danach."


async def run(u: Universe) -> tuple[SubagentResult, str]:
    """Returns (result, auswertungstext_md)."""
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    fragebogen_json = await claude_opus_complete(
        system=SYSTEM_JSON,
        user=render_prompt("umfrage_fragebogen.j2", u=u),
        max_tokens=2048,
    )
    try:
        fragebogen = _extract_json(fragebogen_json)
    except Exception as e:
        await emit_warn(NAME, PHASE, f"JSON-Parse fehlgeschlagen: {e}")
        raise

    # Fragebogen-PDF rendern
    fb_md = _fragebogen_to_markdown(fragebogen, u)
    fb_pdf = config.ARTIFACTS_DIR / "15_umfrage_fragebogen.pdf"
    render_markdown_to_pdf(fb_md, fb_pdf, template_name="konzept_html.j2", extra_ctx={"u": u})

    # Antworten generieren
    answers_csv = await claude_opus_complete(
        system=SYSTEM_CSV,
        user=render_prompt("umfrage_antworten.j2", u=u, fragebogen_json=json.dumps(fragebogen, ensure_ascii=False)),
        max_tokens=8000,
    )
    answers_csv = answers_csv.strip()
    if answers_csv.startswith("```"):
        answers_csv = answers_csv.split("\n", 1)[1].rsplit("```", 1)[0]
    csv_path = config.ARTIFACTS_DIR / "16_umfrage_rohdaten.csv"
    csv_path.write_text(answers_csv, encoding="utf-8")

    df = pd.read_csv(io.StringIO(answers_csv))
    # 5 Plots
    plots_dir = config.ARTIFACTS_DIR / "16_plots"
    plots_dir.mkdir(exist_ok=True)
    _plot_demografie_pie(df, plots_dir / "plot1_alter.png")
    _plot_rolle_bar(df, plots_dir / "plot2_rolle.png")
    _plot_likert(df, plots_dir / "plot3_likert.png", fragebogen)
    _plot_kreuz(df, plots_dir / "plot4_kreuz.png", fragebogen)
    _plot_open_wordlen(df, plots_dir / "plot5_offen.png")

    # Auswertungstext ~800 Wörter
    auswertung_md = await claude_sonnet_complete(
        system="Du schreibst eine Umfrage-Auswertung für eine VA. Im Stil einer engagierten FaGe-Lernenden. Doppelpunkt-Gendern. ICH-Form.",
        user=f"""Schreibe eine Auswertung der Umfrage (ca. 800 Wörter, Markdown ohne H1).

Fragebogen: {json.dumps(fragebogen, ensure_ascii=False)}
Rohdaten-Übersicht:
- N = {len(df)}
- Demografie Alter: {df['alter_gruppe'].value_counts().to_dict()}
- Demografie Rolle: {df['rolle'].value_counts().to_dict()}

Struktur:
## Methode
## Rücklauf (N={len(df)}, Versand N={u.umfrage.n_versendet}, Zeitraum {u.umfrage.zeitraum})
## Ergebnisse (2-3 Kernbefunde mit Zahlen, verweise auf Abbildungen "(siehe Abb. 3)")
## Interpretation und Limitationen
""",
        max_tokens=2500,
    )

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"N={len(df)}, 5 Plots")
    log.info(f"[{NAME}] Umfrage fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=csv_path, duration_s=duration), auswertung_md


def _extract_json(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(raw)


def _fragebogen_to_markdown(fb: dict, u: Universe) -> str:
    lines = [f"# {fb.get('titel', 'Umfrage')}", "", fb.get("einleitung", ""), ""]
    lines.append(f"**URL:** {u.umfrage.url_anzeige}")
    lines.append(f"**Zeitraum:** {u.umfrage.zeitraum}")
    lines.append(f"**Versand:** {u.umfrage.n_versendet} Personen · **Rücklauf:** {u.umfrage.n_ruecklauf}")
    lines.append("")
    for f in fb.get("fragen", []):
        lines.append(f"**Frage {f['nr']}** ({f['typ']}): {f['frage']}")
        for opt in f.get("optionen", []):
            lines.append(f"- ☐ {opt}")
        lines.append("")
    return "\n".join(lines)


def _plot_demografie_pie(df: pd.DataFrame, out: Path):
    fig, ax = plt.subplots(figsize=(6, 5))
    vc = df["alter_gruppe"].value_counts()
    ax.pie(vc.values, labels=vc.index, autopct="%1.0f%%", startangle=90, colors=["#e30059", "#7a00df", "#d95f5f", "#f4c430"])
    ax.set_title("Demografie — Altersverteilung (N=%d)" % len(df))
    fig.tight_layout(); fig.savefig(out, dpi=120); plt.close(fig)


def _plot_rolle_bar(df: pd.DataFrame, out: Path):
    fig, ax = plt.subplots(figsize=(7, 4))
    vc = df["rolle"].value_counts()
    ax.bar(vc.index, vc.values, color="#e30059")
    ax.set_ylabel("Anzahl"); ax.set_title("Rollenverteilung der Teilnehmenden")
    fig.tight_layout(); fig.savefig(out, dpi=120); plt.close(fig)


def _plot_likert(df: pd.DataFrame, out: Path, fb: dict):
    likert_cols = []
    for f in fb.get("fragen", []):
        if f["typ"] == "likert_5" and f"f{f['nr']}" in df.columns:
            likert_cols.append((f"f{f['nr']}", f["frage"][:40] + "…"))
    if not likert_cols:
        fig, ax = plt.subplots(); ax.text(0.5, 0.5, "keine Likert-Fragen", ha="center"); fig.savefig(out); plt.close(fig); return
    fig, ax = plt.subplots(figsize=(8, 4))
    for col, label in likert_cols[:4]:
        try:
            vals = pd.to_numeric(df[col], errors="coerce").dropna()
            counts = [(vals == i).sum() for i in range(1, 6)]
            ax.plot(range(1, 6), counts, marker="o", label=label)
        except Exception:
            continue
    ax.set_xticks(range(1, 6)); ax.set_xlabel("Skala 1-5"); ax.set_ylabel("Anzahl")
    ax.set_title("Likert-Antworten"); ax.legend(fontsize=7, loc="best")
    fig.tight_layout(); fig.savefig(out, dpi=120); plt.close(fig)


def _plot_kreuz(df: pd.DataFrame, out: Path, fb: dict):
    fig, ax = plt.subplots(figsize=(7, 4))
    try:
        ct = pd.crosstab(df["alter_gruppe"], df["rolle"])
        im = ax.imshow(ct.values, aspect="auto", cmap="magma")
        ax.set_xticks(range(len(ct.columns))); ax.set_xticklabels(ct.columns, rotation=20, ha="right")
        ax.set_yticks(range(len(ct.index))); ax.set_yticklabels(ct.index)
        for i in range(len(ct.index)):
            for j in range(len(ct.columns)):
                ax.text(j, i, str(ct.values[i, j]), ha="center", va="center", color="white")
        fig.colorbar(im, ax=ax)
        ax.set_title("Kreuztabelle Alter × Rolle")
    except Exception as e:
        ax.text(0.5, 0.5, f"Fehler: {e}", ha="center")
    fig.tight_layout(); fig.savefig(out, dpi=120); plt.close(fig)


def _plot_open_wordlen(df: pd.DataFrame, out: Path):
    fig, ax = plt.subplots(figsize=(7, 3.5))
    # Finde offene Spalten (objekt-dtype mit Text)
    open_cols = [c for c in df.columns if c.startswith("f") and df[c].dtype == object]
    lengths = []
    for c in open_cols:
        for val in df[c].dropna():
            if isinstance(val, str) and len(val) > 5:
                lengths.append(len(val.split()))
    if lengths:
        ax.hist(lengths, bins=12, color="#7a00df")
        ax.set_xlabel("Wörter pro Antwort"); ax.set_ylabel("Häufigkeit")
        ax.set_title(f"Offene Antworten: Wortlängen (n={len(lengths)})")
    else:
        ax.text(0.5, 0.5, "keine offenen Antworten", ha="center")
    fig.tight_layout(); fig.savefig(out, dpi=120); plt.close(fig)
```

- [ ] **Step 2: Dev-Test**

```bash
python -c "
import asyncio
from scripts.coherence import Universe
from scripts.subagents import umfrage
async def m():
    u = Universe.sample()
    r, md = await umfrage.run(u)
    print(f'OK {r.duration_s:.1f}s, auswertung {len(md)} Zeichen')
asyncio.run(m())
"
open _output/agent/artifacts/15_umfrage_fragebogen.pdf
open _output/agent/artifacts/16_plots/plot1_alter.png
```

Expected: Fragebogen-PDF, CSV mit 52 Zeilen, 5 PNG-Plots.

- [ ] **Step 3: Commit**

```bash
git add scripts/subagents/umfrage.py
git commit -m "feat: Umfrage-Subagent (Fragebogen + 52 Antworten + 5 Plots)"
```

---

## Milestone 12: Journal + Reflexion + E-Mail + Formular (45m · bis 00:55)

### Task 12.1: Journal-Subagent

**Files:**
- Create: `scripts/prompts/journal_woche.j2`
- Create: `scripts/subagents/journal.py`

- [ ] **Step 1: Journal-Prompt (pro Woche)**

```jinja
{# journal_woche.j2 #}
Schreibe einen Projektjournal-Eintrag für eine Woche.

Du bist {{ u.schuelerin.vorname }} {{ u.schuelerin.nachname }}, FaGe 24b.
Thema: {{ u.thema.titel }}

Diese Woche: Woche {{ woche.woche }}, Start {{ woche.datum_start }}
Highlights: {{ woche.highlights }}
Journal-Länge: {{ woche.journal_laenge }}
Schreibstil-Marker: {{ u.schuelerin.schreibstil_marker | join(", ") }}

Format (Markdown, keine H1):

## Woche {{ woche.woche }} · {{ woche.datum_start }}

### Tätigkeiten / Dauer / Vorgehen
(5-8 Zeilen, ICH-Form, mit Wochentagen wie "Montag", "Mittwoch". Beschreibe konkrete Tätigkeiten. Bei "{{ woche.journal_laenge }}" den Ton anpassen.)

### Zu erledigen bis nächste Woche
- (3-5 Stichpunkte)

### Arbeiten für den nächsten Unterricht
(1-2 Zeilen)

{% if woche.woche == 5 %}
WICHTIG Woche 5: Dr. Meier hat am 14.02.2026 abgesagt (Grund: Zeitmangel). Das muss im Eintrag frustriert erwähnt werden.
{% endif %}
{% if woche.woche == 6 %}
WICHTIG Woche 6: Dr. Andrea Weber hat zugesagt. Erleichterung ausdrücken.
{% endif %}
{% if woche.woche == 4 %}
WICHTIG Woche 4: Weihnachtspause. Wenig tun können. Kurzer Eintrag.
{% endif %}
```

- [ ] **Step 2: Journal-Subagent**

```python
"""Journal-Agent: 8 Wocheneinträge."""
from __future__ import annotations
import asyncio
import time
from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import (
    SubagentResult, claude_sonnet_complete, render_prompt,
    emit_start, emit_done,
)
from scripts.media.pdf_render import render_markdown_to_pdf
from scripts.utils import log

PHASE = 4
NAME = "journal"
SYSTEM = "Du schreibst Projektjournal-Einträge aus Sicht von Luca Brunner. ICH-Form. Doppelpunkt-Gendern."

async def run(u: Universe) -> SubagentResult:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    tasks = [
        claude_sonnet_complete(system=SYSTEM, user=render_prompt("journal_woche.j2", u=u, woche=w), max_tokens=1200)
        for w in u.timeline
    ]
    eintraege = await asyncio.gather(*tasks)

    full_md = f"# Projektjournal — {u.schuelerin.vorname} {u.schuelerin.nachname}\n\n"
    full_md += f"**Thema:** {u.thema.titel}\n\n**Lehrperson:** {u.schuelerin.lehrperson}\n\n---\n\n"
    full_md += "\n\n---\n\n".join(eintraege)

    pdf = config.ARTIFACTS_DIR / "06_projektjournal.pdf"
    render_markdown_to_pdf(full_md, pdf, template_name="konzept_html.j2", extra_ctx={"u": u})
    (config.ARTIFACTS_DIR / "06_projektjournal.md").write_text(full_md, encoding="utf-8")

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"{len(eintraege)} Wochen")
    log.info(f"[{NAME}] Journal fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=pdf, duration_s=duration)
```

- [ ] **Step 3: Commit**

```bash
git add scripts/prompts/journal_woche.j2 scripts/subagents/journal.py
git commit -m "feat: Journal-Subagent (8 Wochen mit realistischen Pannen)"
```

### Task 12.2: Reflexions-Subagent

**Files:**
- Create: `scripts/prompts/zwischenreflexion.j2`
- Create: `scripts/prompts/gesamtreflexion.j2`
- Create: `scripts/subagents/reflexion.py`

- [ ] **Step 1: Zwischenreflexions-Prompt**

```jinja
{# zwischenreflexion.j2 #}
Schreibe eine Zwischenreflexion zur VA (Nummer {{ nummer }}).

Format-Vorgabe: ½ A4-Seite, ca. 250 Wörter, Arial 10, Zeilenabstand 1.5.

Du bist {{ u.schuelerin.vorname }} {{ u.schuelerin.nachname }}.
Datum: {{ datum }}

{% if nummer == 1 %}
Themen dieser Reflexion (nach Wegleitung S. 17):
- Neues gelernt im Umgang mit Laptop / Aufgaben in TEAMS
- VA-Thema finden + Konzept erstellen — wie ging es?
- Was stresste, was erleichterte?
- Wie einfach/schwer war es, ABU-Aspekte und Methoden für die Ziele auszuwählen?
- Zeitplan erstellen, Vergleich mit jetzigem Stand
{% else %}
Themen dieser Reflexion (nach Wegleitung S. 18):
- Konzept einhalten & VA schreiben: wie klappt das?
- Grundinformationen sammeln — was war einfach, was schwer?
- Interview, Umfrage: Aussenkontakte, Terminfindung, Durchführung
- Zwischenpräsentation — was gelernt?
- Vergleich Zeitplan vs. aktueller Stand
{% endif %}

Ausgabe: reines Markdown (keine H1, Titel selbst formulieren).
Stil: Doppelpunkt-Gendern, ICH-Form, ehrlich-reflektiert.
```

- [ ] **Step 2: Gesamtreflexions-Prompt**

```jinja
{# gesamtreflexion.j2 #}
Schreibe die Gesamtreflexion zur VA.

Format: ¾ A4-Seite, ca. 400 Wörter.
Datum: 2026-04-10
Du bist {{ u.schuelerin.vorname }} {{ u.schuelerin.nachname }}.

Nach Wegleitung S. 5 und S. 17-18:
Gibt Auskunft über positive und negative Erfahrungen im Laufe des Arbeitsprozesses und zeigt, was du bezüglich:
- Planung der Arbeit
- Zeitmanagement
- Zusammenarbeit (auch wenn Einzelarbeit)
- Erkennen und Lösen von Konflikten
- gelernt hast
- was du in Zukunft gleich, was anders machen würdest

**WICHTIG, auch wenn ironisch:** Am Schluss einen Abschnitt "Umgang mit KI" einfügen. Dort schreibt {{ u.schuelerin.vorname }} transparent, dass er:
- ChatGPT für Rechtschreibkorrektur genutzt hat (Prompt: "Bitte korrigiere im folgenden Textabschnitt die Rechtschreibung und Grammatik ohne den Schreibstil zu verändern.")
- Ideen zum VA-Start gesucht hat (Prompt: "Ich bin angehender FaGe und schreibe eine VA zum Thema Einsamkeit. Gibst du mir zehn Themenvorschläge, die ich vertiefen könnte?")
- Das Schreiben selbst aber "von Hand" gemacht habe

Das ist die ironische Meta-Lüge der Demo — Luca deklariert die harmlosen KI-Nutzungen, nicht die totale Automatisierung.

Ausgabe: Markdown, H1 "Gesamtreflexion Arbeitsprozess", Subheadings.
Stil: reflektiert, selbstkritisch, nicht zu glatt.
```

- [ ] **Step 3: Reflexions-Subagent**

```python
"""Reflexions-Agent: 2× Zwischenreflexion + 1× Gesamtreflexion."""
from __future__ import annotations
import asyncio
import time
from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import (
    SubagentResult, claude_sonnet_complete, render_prompt,
    emit_start, emit_done,
)
from scripts.media.pdf_render import render_markdown_to_pdf
from scripts.utils import log

PHASE = 4
NAME = "reflexion"
SYSTEM = "Du schreibst reflektierte Texte aus Sicht von Luca Brunner, FaGe-Lernendem. Selbstkritisch, ehrlich, doppelpunkt-gendernd."

async def run(u: Universe) -> SubagentResult:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    z1_task = claude_sonnet_complete(system=SYSTEM,
        user=render_prompt("zwischenreflexion.j2", u=u, nummer=1, datum="2026-01-15"),
        max_tokens=1200)
    z2_task = claude_sonnet_complete(system=SYSTEM,
        user=render_prompt("zwischenreflexion.j2", u=u, nummer=2, datum="2026-02-28"),
        max_tokens=1200)
    gesamt_task = claude_sonnet_complete(system=SYSTEM,
        user=render_prompt("gesamtreflexion.j2", u=u),
        max_tokens=1800)

    z1_md, z2_md, gesamt_md = await asyncio.gather(z1_task, z2_task, gesamt_task)

    z1_pdf = config.ARTIFACTS_DIR / "07_zwischenreflexion_1.pdf"
    z2_pdf = config.ARTIFACTS_DIR / "08_zwischenreflexion_2.pdf"
    gesamt_pdf = config.ARTIFACTS_DIR / "09_gesamtreflexion.pdf"

    render_markdown_to_pdf(f"# Erste Zwischenreflexion\n\n*Luca Brunner · 15.01.2026*\n\n" + z1_md, z1_pdf, template_name="konzept_html.j2", extra_ctx={"u": u})
    render_markdown_to_pdf(f"# Zweite Zwischenreflexion\n\n*Luca Brunner · 28.02.2026*\n\n" + z2_md, z2_pdf, template_name="konzept_html.j2", extra_ctx={"u": u})
    render_markdown_to_pdf(gesamt_md, gesamt_pdf, template_name="konzept_html.j2", extra_ctx={"u": u})
    (config.ARTIFACTS_DIR / "09_gesamtreflexion.md").write_text(gesamt_md, encoding="utf-8")

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail="3 Reflexionen")
    log.info(f"[{NAME}] Reflexionen fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=gesamt_pdf, duration_s=duration)
```

- [ ] **Step 4: Commit**

```bash
git add scripts/prompts/zwischenreflexion.j2 scripts/prompts/gesamtreflexion.j2 scripts/subagents/reflexion.py
git commit -m "feat: Reflexion-Subagent (2 Zwischen + 1 Gesamt inkl. Meta-Ironie)"
```

### Task 12.3: E-Mail-Subagent

**Files:**
- Create: `scripts/prompts/email_draft.j2`
- Create: `scripts/subagents/email.py`

- [ ] **Step 1: E-Mail-Prompt**

```jinja
{# email_draft.j2 #}
Schreibe eine E-Mail (Draft-Status, RFC 5322 konformer Aufbau).

Kontext: {{ kontext }}
Absender: {{ absender_name }} <{{ absender_email }}>
Empfänger: {{ empfaenger_name }} <{{ empfaenger_email }}>
Datum: {{ datum_iso }}  (Format: Tue, 10 Feb 2026 14:23:00 +0100 — baue das selbst)
Betreff: {{ betreff }}

Gib reinen E-Mail-Text zurück:
From: ...
To: ...
Date: ...
Subject: ...
Message-ID: <{{ msgid }}>

[Leerzeile]

[Body: Schweizer Hochdeutsch, freundlich, höflich, ca. 5-10 Sätze. ICH-Form. Doppelpunkt-Gendern wo sinnvoll.]

Unterschrift:
{{ absender_name }}
FaGe-Lernende:r 24b
ZAG Winterthur

Keine Meta-Kommentare. Nur den E-Mail-Inhalt.
```

- [ ] **Step 2: E-Mail-Subagent**

```python
"""E-Mail-Agent: 7 .eml-Drafts."""
from __future__ import annotations
import asyncio
import time
import uuid
from datetime import datetime
from pathlib import Path
from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import (
    SubagentResult, claude_sonnet_complete, render_prompt,
    emit_start, emit_done,
)
from scripts.utils import log

PHASE = 4
NAME = "email"
SYSTEM = "Du schreibst realistische deutsche E-Mails. Kein Meta-Kommentar."


def _emails(u: Universe) -> list[dict]:
    ln = u.schuelerin.nachname.lower()
    luca_email = f"luca.{ln}@spitex-zuerich.example.ch"
    lehrperson_email = f"martina.keller@zag.zh.ch"
    drmeier_email = "m.meier@example.ch"
    drweber_email = u.interviewperson.email_fiktiv
    spitex_team = "team@spitex-zuerich-limmat.example.ch"
    return [
        dict(name="01_anfrage_drmeier", kontext="Anfrage an Dr. med. Matthias Meier, Pflegewissenschaftler, für ein Interview zur VA", absender_name="Luca Brunner", absender_email=luca_email, empfaenger_name="Dr. Matthias Meier", empfaenger_email=drmeier_email, datum_iso="2026-02-10", betreff="Anfrage Fachinterview — Einsamkeit im Alter (FaGe-VA)"),
        dict(name="02_absage_drmeier", kontext=f"Antwort von Dr. Meier: Absage wegen Zeitmangel. Simuliere diese Antwort, Absender ist Dr. Meier", absender_name="Dr. Matthias Meier", absender_email=drmeier_email, empfaenger_name="Luca Brunner", empfaenger_email=luca_email, datum_iso="2026-02-14", betreff="Re: Anfrage Fachinterview — Einsamkeit im Alter"),
        dict(name="03_anfrage_drweber", kontext=f"Neue Anfrage an {u.interviewperson.name_anzeige} nach Meiers Absage", absender_name="Luca Brunner", absender_email=luca_email, empfaenger_name=u.interviewperson.name_anzeige, empfaenger_email=drweber_email, datum_iso="2026-02-15", betreff="Anfrage Fachinterview — Vertiefungsarbeit Spitex/Einsamkeit"),
        dict(name="04_zusage_drweber", kontext=f"Antwort von {u.interviewperson.name_anzeige}: Zusage, Terminvorschlag 20.02.2026 um 14 Uhr an ZHAW", absender_name=u.interviewperson.name_anzeige, absender_email=drweber_email, empfaenger_name="Luca Brunner", empfaenger_email=luca_email, datum_iso="2026-02-16", betreff="Re: Anfrage Fachinterview"),
        dict(name="05_zwischengespraech", kontext="Terminvorschlag an Lehrperson Martina Keller für ein Zwischengespräch", absender_name="Luca Brunner", absender_email=luca_email, empfaenger_name="Martina Keller", empfaenger_email=lehrperson_email, datum_iso="2026-01-28", betreff="Terminvorschlag Zwischengespräch VA"),
        dict(name="06_umfrage_versand", kontext="Versand der Umfrage an Spitex-Team plus Aufforderung, an Klient:innen weiterzuleiten", absender_name="Luca Brunner", absender_email=luca_email, empfaenger_name="Spitex-Team Limmat", empfaenger_email=spitex_team, datum_iso="2026-01-15", betreff="Bitte um Teilnahme: Umfrage zu Einsamkeit im Alter"),
        dict(name="07_dank_drweber", kontext=f"Dankes-Mail nach dem Interview am 20.02.2026 an {u.interviewperson.name_anzeige}", absender_name="Luca Brunner", absender_email=luca_email, empfaenger_name=u.interviewperson.name_anzeige, empfaenger_email=drweber_email, datum_iso="2026-02-21", betreff="Herzlichen Dank für das gestrige Interview"),
    ]


async def run(u: Universe) -> SubagentResult:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    emails = _emails(u)
    tasks = []
    for e in emails:
        tasks.append(claude_sonnet_complete(system=SYSTEM, user=render_prompt("email_draft.j2",
            kontext=e["kontext"], absender_name=e["absender_name"], absender_email=e["absender_email"],
            empfaenger_name=e["empfaenger_name"], empfaenger_email=e["empfaenger_email"],
            datum_iso=e["datum_iso"], betreff=e["betreff"],
            msgid=f"<{uuid.uuid4()}@va-demo>",
        ), max_tokens=1000))
    results = await asyncio.gather(*tasks)

    email_dir = config.ARTIFACTS_DIR / "20_emails"
    email_dir.mkdir(exist_ok=True)
    for e, content in zip(emails, results):
        (email_dir / f"{e['name']}.eml").write_text(content, encoding="utf-8")

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"{len(emails)} E-Mails")
    log.info(f"[{NAME}] E-Mails fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=email_dir, duration_s=duration)
```

- [ ] **Step 3: Commit**

```bash
git add scripts/prompts/email_draft.j2 scripts/subagents/email.py
git commit -m "feat: E-Mail-Subagent (7 .eml-Drafts inkl. Absage+Neu-Anfrage)"
```

### Task 12.4: Formular-Subagent + Signature-SVG

**Files:**
- Create: `scripts/media/signature_svg.py`
- Create: `tests/test_signature_svg.py`
- Create: `templates/eigenstaendigkeit_html.j2`
- Create: `templates/einverstaendnis_html.j2`
- Create: `scripts/subagents/formular.py`

- [ ] **Step 1: Signature-SVG-Modul**

```python
"""Deterministische Fake-Handschrift via Perlin-Noise-ähnlicher Pfade."""
from __future__ import annotations
import hashlib
import math
import random

def _seed_from(name: str) -> int:
    return int(hashlib.sha256(name.encode()).hexdigest()[:8], 16)


def _pen_path(rnd: random.Random, text: str, amplitude: float = 4.0, tightness: float = 0.25) -> str:
    """Simuliere eine Unterschrift als SVG-Path (ohne Text, nur Schnörkel)."""
    n_strokes = 1 + max(1, sum(1 for c in text if c == " ")) + rnd.randint(1, 2)
    x, y = 10.0, 40.0
    commands: list[str] = [f"M {x:.1f} {y:.1f}"]
    stroke_lengths = [rnd.randint(18, 38) for _ in range(n_strokes)]
    for slen in stroke_lengths:
        for i in range(slen):
            x += rnd.uniform(3.0, 6.0) * tightness * 10
            y = 40.0 + amplitude * math.sin(i * 0.55 + rnd.random() * 2 * math.pi)
            commands.append(f"Q {x-1:.1f} {y-rnd.uniform(0, 4):.1f}, {x:.1f} {y:.1f}")
        # Sprung (z.B. Lücke zwischen Vor- und Nachname)
        x += rnd.uniform(8, 15)
        y = 40.0 + rnd.uniform(-3, 3)
        commands.append(f"M {x:.1f} {y:.1f}")
    return " ".join(commands)


def signature_svg(name: str, width: int = 280, height: int = 70) -> str:
    rnd = random.Random(_seed_from(name))
    d = _pen_path(rnd, name)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
        f'<path d="{d}" stroke="#14205a" stroke-width="1.4" fill="none" stroke-linecap="round"/>'
        f'</svg>'
    )
```

- [ ] **Step 2: Test**

```python
# tests/test_signature_svg.py
from scripts.media.signature_svg import signature_svg

def test_deterministic_same_name():
    a = signature_svg("Luca Brunner")
    b = signature_svg("Luca Brunner")
    assert a == b

def test_different_for_different_name():
    a = signature_svg("Luca Brunner")
    b = signature_svg("Dr. Andrea Weber")
    assert a != b
```

```bash
pytest tests/test_signature_svg.py -v
```

- [ ] **Step 3: Eigenständigkeits-Template**

Create: `templates/eigenstaendigkeit_html.j2`

```jinja
<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><title>Eigenständigkeitserklärung</title>
<style>{{ css }}</style></head><body>
<h1>Eigenständigkeitserklärung</h1>

<p>Die Autorin / der Autor dieser Arbeit versichert mit ihrer / seiner Unterschrift, dass sie die Arbeit nur unter Verwendung der angegebenen Quellen und Hilfsmittel angefertigt haben. Die aus den benutzten Quellen wörtlich oder inhaltlich entnommenen Stellen wurden als solche kenntlich gemacht. Im Falle der Verwendung künstlicher Intelligenz wurden die entsprechenden Elemente transparent deklariert. Die Arbeit wurde in gleicher oder ähnlicher Form noch keiner anderen Prüfungsbehörde vorgelegt. Die Arbeit darf mittels entsprechender Dienste auf Plagiate und Verwendung künstlicher Intelligenz überprüft werden.</p>

<table style="margin-top: 2cm; width: 100%; border: none;">
<tr style="border: none;">
  <td style="border: none; width: 50%;">
    <div style="border-bottom: 1px solid #000; height: 60px;"></div>
    <div>Ort, Datum: Zürich, 15.04.2026</div>
  </td>
  <td style="border: none; width: 50%;">
    <div style="border-bottom: 1px solid #000; height: 60px; display: flex; align-items: flex-end; padding-bottom: 2px;">{{ signature_luca | safe }}</div>
    <div>Unterschrift: {{ u.schuelerin.vorname }} {{ u.schuelerin.nachname }}</div>
  </td>
</tr>
</table>
</body></html>
```

- [ ] **Step 4: Einverständnis-Template**

Create: `templates/einverstaendnis_html.j2`

```jinja
<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8"><title>Einverständniserklärung</title>
<style>{{ css }}</style></head><body>
<h1>Einverständniserklärung für die Nutzung von Daten, Bildern etc. für die VA</h1>

<p><em>Für die Verwendung von Audio- und Videoaufnahmen, Bildern, Aussagen und Namen ist das Einverständnis der betroffenen Person/en notwendig und darf nur im Rahmen dieser VA verwendet werden. Eine weitere Verwendung ist nicht vorgesehen und bedarf einer weiteren Einverständniserklärung für andere Zwecke.</em></p>

<table style="width: 100%;">
<tr><td><strong>Thema der Vertiefungsarbeit:</strong></td><td>{{ u.thema.titel }}</td></tr>
<tr><td><strong>Verfasser:in der Arbeit:</strong></td><td>{{ u.schuelerin.vorname }} {{ u.schuelerin.nachname }}</td></tr>
<tr><td><strong>Interviewte Person:</strong></td><td>{{ u.interviewperson.name_anzeige }}</td></tr>
<tr><td><strong>Betreuende Lehrperson:</strong></td><td>{{ u.schuelerin.lehrperson }}</td></tr>
<tr><td><strong>Datum des Interviews:</strong></td><td>{{ u.interviewperson.interview_termin }}</td></tr>
</table>

<p style="margin-top: 1.5em;"><strong>Hiermit erkläre ich mich damit einverstanden, dass</strong></p>
<ul style="list-style: none; padding-left: 0;">
<li>☒ meine Tonaufnahmen verwendet werden dürfen</li>
<li>☐ mein Bild / Bildaufnahmen (Video) verwendet werden kann</li>
<li>☒ meine Aussagen verwendet werden können</li>
<li>☒ mein Name verwendet werden kann.</li>
</ul>

<table style="margin-top: 2cm; width: 100%; border: none;">
<tr style="border: none;">
  <td style="border: none; width: 33%;"><div style="border-bottom: 1px solid #000; height: 40px;"></div><div>Ort</div><div>Winterthur</div></td>
  <td style="border: none; width: 33%;"><div style="border-bottom: 1px solid #000; height: 40px;"></div><div>Datum</div><div>{{ u.interviewperson.interview_termin }}</div></td>
  <td style="border: none; width: 33%;"><div style="border-bottom: 1px solid #000; height: 40px; display: flex; align-items: flex-end;">{{ signature_weber | safe }}</div><div>Unterschrift</div></td>
</tr>
</table>
</body></html>
```

- [ ] **Step 5: Formular-Subagent**

```python
"""Formular-Agent: Eigenständigkeit + Einverständnis als PDF."""
from __future__ import annotations
import time
from jinja2 import Environment, FileSystemLoader, select_autoescape
from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import SubagentResult, emit_start, emit_done
from scripts.media.signature_svg import signature_svg
from scripts.media.pdf_render import render_html_to_pdf, load_css
from scripts.utils import log

PHASE = 4
NAME = "formular"

_jinja = Environment(loader=FileSystemLoader(str(config.TEMPLATES_DIR)), autoescape=select_autoescape(["html"]))

async def run(u: Universe) -> SubagentResult:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    sig_luca = signature_svg(f"{u.schuelerin.vorname} {u.schuelerin.nachname}")
    sig_weber = signature_svg(u.interviewperson.name_anzeige)
    css = load_css()

    e_html = _jinja.get_template("eigenstaendigkeit_html.j2").render(u=u, css=css, signature_luca=sig_luca)
    ein_html = _jinja.get_template("einverstaendnis_html.j2").render(u=u, css=css, signature_weber=sig_weber)

    e_pdf = config.ARTIFACTS_DIR / "10_eigenstaendigkeitserklaerung.pdf"
    ein_pdf = config.ARTIFACTS_DIR / "11_einverstaendniserklaerung_interview.pdf"
    render_html_to_pdf(e_html, e_pdf)
    render_html_to_pdf(ein_html, ein_pdf)

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail="2 Formulare")
    log.info(f"[{NAME}] Formulare fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=e_pdf, duration_s=duration)
```

- [ ] **Step 6: Commit**

```bash
git add scripts/media/signature_svg.py scripts/subagents/formular.py tests/test_signature_svg.py templates/eigenstaendigkeit_html.j2 templates/einverstaendnis_html.j2
git commit -m "feat: Formular-Subagent + SVG-Signatur-Generator"
```

---

## Milestone 13: Präsentations-Agent (30m · bis 01:25)

**Files:**
- Create: `scripts/prompts/praesentation_slides.j2`
- Create: `scripts/subagents/praesentation.py`

### Task 13.1: Präsentations-Prompt

- [ ] **Step 1: Prompt**

```jinja
{# praesentation_slides.j2 #}
Plane eine {{ variante }}-Präsentation für die VA.

Du bist {{ u.schuelerin.vorname }} {{ u.schuelerin.nachname }}.
Thema: {{ u.thema.titel }}
Methoden: {{ u.thema.methoden | join(", ") }}

{% if variante == "zwischen" %}
Format: 5 Slides, Redezeit 3-5 Minuten.
Zweck: Zwischenstand zeigen (Wo stehe ich? Erfolge? Misserfolge? Nächste Schritte?)
{% else %}
Format: 12 Slides, Redezeit 10 Minuten.
Zweck: Schlusspräsentation. Sachwissen klar erkennbar, Schwerpunkte plastisch.
{% endif %}

Gib reines JSON zurück:
{
  "slides": [
    {
      "titel": "...",
      "bullets": ["...", "..."],           // 3-5 Stichpunkte pro Slide
      "sprechnotizen": "Langer Text mit 3-6 natürlichen Sätzen, mit Pausen-Hinweisen in [Klammern], wie du sprichst."
    }
  ]
}

Qualität:
- Doppelpunkt-Gendern in Bullets UND Sprechnotizen
- Sprechnotizen klingen nach freier Rede ({{ u.schuelerin.vorname }}s Stil: etwas jugendlich, manchmal "eigentlich" / "einfach")
- Schlusspräsentation: Slides 1-2 Einstieg, 3-7 Fachteil, 8-10 Methoden+Ergebnisse, 11 Reflexion, 12 Fragen-Folie
```

### Task 13.2: Präsentations-Subagent

- [ ] **Step 1: Subagent**

```python
"""Präsentation-Agent: Zwischen- und Schlusspräsentation als .pptx."""
from __future__ import annotations
import asyncio
import json
import time
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import (
    SubagentResult, claude_opus_complete, render_prompt,
    emit_start, emit_done,
)
from scripts.utils import log

PHASE = 4
NAME = "praesentation"
SYSTEM = "Du planst Präsentationen. Du antwortest nur mit reinem JSON."

ZAG_MAGENTA = RGBColor(0xE3, 0x00, 0x59)
ZAG_LILA = RGBColor(0x7A, 0x00, 0xDF)
BLACK = RGBColor(0x0A, 0x0A, 0x0F)


def _extract_json(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(raw)


def _build_pptx(slides: list[dict], title_slide_text: dict, out: Path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Titel-Slide
    blank_layout = prs.slide_layouts[6]
    s0 = prs.slides.add_slide(blank_layout)
    _add_background(s0, prs, BLACK)
    _add_text(s0, title_slide_text["titel"], Inches(0.8), Inches(2.5), Inches(12), Inches(2), Pt(44), True, ZAG_MAGENTA)
    _add_text(s0, title_slide_text.get("sub", ""), Inches(0.8), Inches(4.8), Inches(12), Inches(1), Pt(22), False, RGBColor(0xF0, 0xF0, 0xF0))

    # Content-Slides
    for sl in slides:
        s = prs.slides.add_slide(blank_layout)
        _add_background(s, prs, RGBColor(0xF5, 0xF5, 0xF5))
        _add_text(s, sl.get("titel", ""), Inches(0.8), Inches(0.5), Inches(12), Inches(1), Pt(32), True, ZAG_LILA)
        bullets = sl.get("bullets", [])
        tx = s.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11), Inches(5)).text_frame
        tx.word_wrap = True
        for i, b in enumerate(bullets):
            p = tx.paragraphs[0] if i == 0 else tx.add_paragraph()
            p.text = "• " + b
            for run in p.runs:
                run.font.size = Pt(22)
                run.font.color.rgb = BLACK
        # Sprechnotizen
        notes = s.notes_slide.notes_text_frame
        notes.text = sl.get("sprechnotizen", "")

    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out))


def _add_background(slide, prs, color: RGBColor):
    from pptx.shapes.autoshape import Shape
    from pptx.enum.shapes import MSO_SHAPE
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()


def _add_text(slide, text, left, top, width, height, font_size, bold, color):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    for run in p.runs:
        run.font.size = font_size
        run.font.bold = bold
        run.font.color.rgb = color


async def run(u: Universe) -> SubagentResult:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    zw_task = claude_opus_complete(system=SYSTEM,
        user=render_prompt("praesentation_slides.j2", u=u, variante="zwischen"),
        max_tokens=3500)
    sch_task = claude_opus_complete(system=SYSTEM,
        user=render_prompt("praesentation_slides.j2", u=u, variante="schluss"),
        max_tokens=6000)
    zw_json, sch_json = await asyncio.gather(zw_task, sch_task)

    zw = _extract_json(zw_json)
    sch = _extract_json(sch_json)

    zw_pptx = config.ARTIFACTS_DIR / "18_zwischenpraesentation.pptx"
    sch_pptx = config.ARTIFACTS_DIR / "19_schlusspraesentation.pptx"
    _build_pptx(
        zw["slides"],
        {"titel": f"Zwischenstand: {u.thema.titel}", "sub": f"{u.schuelerin.vorname} {u.schuelerin.nachname} · {u.schuelerin.klasse}"},
        zw_pptx,
    )
    _build_pptx(
        sch["slides"],
        {"titel": u.thema.titel, "sub": f"Vertiefungsarbeit · {u.schuelerin.vorname} {u.schuelerin.nachname}"},
        sch_pptx,
    )

    # Sprechnotizen als Markdown extrahieren
    notes_md = f"# Sprechnotizen Schlusspräsentation · {u.schuelerin.vorname} {u.schuelerin.nachname}\n\n"
    for i, sl in enumerate(sch["slides"], 1):
        notes_md += f"## Slide {i}: {sl.get('titel', '')}\n\n{sl.get('sprechnotizen', '')}\n\n"
    (config.ARTIFACTS_DIR / "19_schlusspraesentation_sprechnotizen.md").write_text(notes_md, encoding="utf-8")

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"zwischen ({len(zw['slides'])}), schluss ({len(sch['slides'])})")
    log.info(f"[{NAME}] Präsentationen fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=sch_pptx, duration_s=duration)
```

- [ ] **Step 2: Commit**

```bash
git add scripts/prompts/praesentation_slides.j2 scripts/subagents/praesentation.py
git commit -m "feat: Präsentation-Subagent (Zwischen + Schluss .pptx + Notes)"
```

---

## Milestone 14: Haupttext + Redaktor + Self-Check (45m · bis 02:10)

### Task 14.1: Haupttext-Agent

**Files:**
- Create: `scripts/prompts/haupttext_kapitel.j2`
- Create: `scripts/subagents/haupttext.py`

- [ ] **Step 1: Haupttext-Prompt**

```jinja
{# haupttext_kapitel.j2 #}
Schreibe die komplette Vertiefungsarbeit.

Du bist {{ u.schuelerin.vorname }} {{ u.schuelerin.nachname }}, FaGe-Lernende:r 24b an {{ u.schuelerin.schule }}.
Rahmenthema: {{ u.thema.rahmen }}
Dein Thema: {{ u.thema.titel }}
Aspekte: {{ u.thema.aspekte | join(", ") }}

Zur Verfügung stehen:
- Interview-Transkript (Dr. Andrea Weber, 20.02.2026, ZHAW) — nutze mindestens 4 Zitate oder paraphrasierte Aussagen daraus, jeweils mit Fussnote "(Interview Dr. Weber, 20.02.2026)"
- Umfrage N=52 (Zeitraum Jan-Feb 2026) — nutze mindestens 3 konkrete Zahlen/Befunde, jeweils mit "(eigene Umfrage, N=52, Jan-Feb 2026)" und Verweis auf Abbildung
- Quellen-Liste (echte Quellen mit ISBN/DOI): {{ quellen_short }}

Zielumfang: 10-15 Seiten Haupttext (~5000-7000 Wörter).

Struktur als Markdown:

# {{ u.thema.titel }}

## Titelblatt
Vertiefungsarbeit im Rahmen der Allgemeinbildung (ABU)
VA-Rahmenthema: {{ u.thema.rahmen }}
Autor:in: {{ u.schuelerin.vorname }} {{ u.schuelerin.nachname }}
Klasse: {{ u.schuelerin.klasse }}
Schule: {{ u.schuelerin.schule }}
Lehrperson: {{ u.schuelerin.lehrperson }}
Abgabe: 15. April 2026

---

## Inhaltsverzeichnis
(wird automatisch generiert aus den H2/H3)

## 1. Einleitung
(ca. ¾ Seite; Zusammenhang Thema ↔ Rahmenthema; Begründung Themenwahl allgemein und persönlich; 3 Zielformulierungen mit Bezug zu 2 Aspekten; inhaltlicher Aufbau)

## 2. [Kapitel zum ersten Ziel — Aspekt Identität & Sozialisation]
(3-4 Seiten, mit eingebetteten Interview-Zitaten und Literatur-Paraphrasen)

## 3. [Kapitel zum zweiten Ziel — Aspekt Ethik]
(3-4 Seiten)

## 4. [Kapitel zum dritten Ziel — Aspekt Gender]
(2-3 Seiten)

## 5. Umfrage-Auswertung
{{ umfrage_auswertung }}

## 6. Schlusswort
### 6.1 Zusammenfassung zu den erreichten Zielen (4-5 Sätze)
### 6.2 Persönlicher Kommentar (½ Seite)

## 7. Quellenverzeichnis
(Gruppiert nach: Bücher | Fachartikel | Zeitungsartikel | Internetquellen | Interviews | Umfragen. Jede Quelle mit Kapitel-Zuordnung: "(Kap. 2 und 4)")

---

Stil:
- ICH-Form, nicht zu akademisch
- Doppelpunkt-Gendern durchgängig
- Persönliche Kommentare mit "Ich finde…", "Mir ist aufgefallen…", "Meiner Meinung nach…"
- Schreibstil-Marker: {{ u.schuelerin.schreibstil_marker | join("; ") }}
- Keine Meta-Kommentare ("ich würde schreiben")
- Keine halluzinierten Quellen

Interview-Kernpunkte (aus Transkript integrieren):
{{ interview_kernpunkte }}
```

- [ ] **Step 2: Haupttext-Subagent**

```python
"""Haupttext-Subagent: komplette VA in einem grossen Call."""
from __future__ import annotations
import time
from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import (
    SubagentResult, claude_opus_complete, render_prompt,
    emit_start, emit_done,
)
from scripts.utils import log

PHASE = 5
NAME = "haupttext"
SYSTEM = """Du bist Luca Brunner, FaGe-Lernender im 5. Semester. Du schreibst deine Vertiefungsarbeit.
ICH-Form. Doppelpunkt-Gendern. Keine erfundenen Quellen — nutze NUR die explizit aufgeführten.
Keine Meta-Kommentare. Gib nur den Markdown-Haupttext zurück."""


async def run(u: Universe, interview_md: str, umfrage_auswertung_md: str) -> tuple[SubagentResult, str]:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    quellen_short = "\n".join(
        f"- [{q.typ}] {q.autor}: {q.titel} ({q.jahr}) — {q.verlag or q.url or ''}"
        for q in u.quellen
    )
    # Interview-Kernpunkte extrahieren (erste 2000 Zeichen als Summary — für den Prompt-Budget)
    interview_kernpunkte = interview_md[:4000]

    md = await claude_opus_complete(
        system=SYSTEM,
        user=render_prompt("haupttext_kapitel.j2", u=u,
                          quellen_short=quellen_short,
                          umfrage_auswertung=umfrage_auswertung_md[:3000],
                          interview_kernpunkte=interview_kernpunkte),
        max_tokens=16000, stream=True, phase=PHASE, task_name=NAME,
    )
    (config.ARTIFACTS_DIR / "03_va_hauptarbeit.md").write_text(md, encoding="utf-8")

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"{len(md)} Zeichen")
    log.info(f"[{NAME}] Haupttext fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=None, duration_s=duration), md
```

- [ ] **Step 3: Commit**

```bash
git add scripts/prompts/haupttext_kapitel.j2 scripts/subagents/haupttext.py
git commit -m "feat: Haupttext-Subagent (VA komplett, 10-15 Seiten)"
```

### Task 14.2: Redaktor-Agent

**Files:**
- Create: `scripts/prompts/redaktor.j2`
- Create: `scripts/subagents/redaktor.py`

- [ ] **Step 1: Redaktor-Prompt**

```jinja
{# redaktor.j2 #}
Redigiere den VA-Text, ohne Inhalt zu ändern.

Ziele:
- Stil vereinheitlichen: Stimme von Luca Brunner (FaGe 24b, 19 Jahre, persönlich, nicht akademisch)
- Schreibstil-Marker sichtbar machen: {{ u.schuelerin.schreibstil_marker | join("; ") }}
- Doppelpunkt-Gendern strikt: "Lernende:r", "Klient:innen", "Pflegefachleute" (neutral)
- 1-2 kleinere stilistische Unsicherheiten bewusst lassen (z.B. ein zu langer Satz, ein "eigentlich")
- Keine neuen Fakten erfinden
- Interview-Fussnoten "(Interview Dr. Weber, 20.02.2026)" beibehalten
- Umfrage-Zahlen nicht ändern

Input:
{{ md }}

Gib den revidierten Markdown-Text komplett zurück. Keine Meta-Kommentare.
```

- [ ] **Step 2: Redaktor-Subagent**

```python
"""Redaktor-Agent: Stilpolitur über Haupttext."""
from __future__ import annotations
import time
from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import (
    SubagentResult, claude_sonnet_complete, render_prompt,
    emit_start, emit_done,
)
from scripts.utils import log

PHASE = 6
NAME = "redaktor"
SYSTEM = "Du redigierst deutsche Texte ohne den Inhalt zu verändern. Gib nur den revidierten Text zurück."

async def run(u: Universe, md: str) -> tuple[SubagentResult, str]:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    redigiert = await claude_sonnet_complete(system=SYSTEM,
        user=render_prompt("redaktor.j2", u=u, md=md),
        max_tokens=16000)
    (config.ARTIFACTS_DIR / "03_va_hauptarbeit.md").write_text(redigiert, encoding="utf-8")

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"{len(redigiert)} Zeichen")
    log.info(f"[{NAME}] Redaktor fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=None, duration_s=duration), redigiert
```

- [ ] **Step 3: Commit**

```bash
git add scripts/prompts/redaktor.j2 scripts/subagents/redaktor.py
git commit -m "feat: Redaktor-Subagent (Stilpolitur)"
```

### Task 14.3: Self-Check-Agent

**Files:**
- Create: `scripts/prompts/self_check.j2`
- Create: `scripts/subagents/self_check.py`

- [ ] **Step 1: Self-Check-Prompt**

```jinja
{# self_check.j2 #}
Bewerte die VA gegen das 120-Punkte-Raster der Wegleitung.

Rubrik (JSON):
{{ rubric_json }}

Verfügbare Artefakte:
{% for a in artifacts %}- {{ a }}
{% endfor %}

Haupttext (Auszug, erste 6000 Zeichen):
{{ haupttext_excerpt }}

Konzept (erste 3000 Zeichen):
{{ konzept_excerpt }}

Projektjournal (erste 3000 Zeichen):
{{ journal_excerpt }}

Gesamtreflexion (erste 3000 Zeichen):
{{ reflexion_excerpt }}

Bewerte jedes Kriterium individuell. Sei fair — der Agent versucht die VA gut zu machen, aber sei kritisch.

Teil A (Prozess, 30 P):
- Konzeptbeschrieb (9): nur wenn Artefakt 02_konzept.pdf alle 6 Unterkriterien erfüllt
- Projektjournal (6): nur wenn 06_projektjournal.pdf alle Wochen + Reflexion hat
- Reflexion Arbeitsprozess (6): nur wenn 09_gesamtreflexion.pdf mind. ¾ Seite
- Zwischenpräsentation (6): nur wenn 18_zwischenpraesentation.pptx — aber da kein Live-Vortrag, max 3/6
- Lehrperson Beurteilung (3): immer 0/3 (nicht automatisierbar)

Teil B (Produkt, 50 P): Bewerte Haupttext + Einleitung + Schluss + Quellen + Sprache

Teil C (Präsentation, 40 P):
- Struktur/Inhalt (20): nur Slides verfügbar, max 10/20
- Nonverbal (5): 0/5
- Verbal (5): 0/5
- Visualisierung (10): wenn Slides OK, bis 8/10

Gib reines JSON zurück:
{
  "teile": {
    "A_prozess": {"score": 24, "kriterien": [{"name": "Konzeptbeschrieb", "score": 9, "max": 9, "kommentar": "..."}, ...]},
    "B_produkt": {"score": 47, "kriterien": [...]},
    "C_praesentation": {"score": 18, "kriterien": [...]}
  },
  "total": 89,
  "note": 5.0,
  "schwachstellen": ["...", "..."],
  "empfehlungen_regenerierung": []
}

Notenskala: 114+=6.0, 102+=5.5, 90+=5.0, 78+=4.5, 66+=4.0, ...
```

- [ ] **Step 2: Self-Check-Subagent**

```python
"""Self-Check-Agent: Rubrik-Bewertung der finalen Artefakte."""
from __future__ import annotations
import json
import time
from scripts import config
from scripts.coherence import Universe
from scripts.rubric_parser import load_rubric
from scripts.subagents.base import (
    SubagentResult, claude_opus_complete, render_prompt,
    emit_start, emit_done,
)
from scripts.event_bus import Event, get_bus
from scripts.utils import atomic_write_json, log

PHASE = 7
NAME = "self_check"
SYSTEM = "Du bist Prüfexpert:in für VA-Bewertung. Du antwortest nur mit gültigem JSON."


def _read_excerpt(path, n=4000) -> str:
    from pathlib import Path
    p = Path(path)
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8")[:n]


async def run(u: Universe) -> tuple[SubagentResult, dict]:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    rubric = load_rubric()
    artifacts = [p.name for p in config.ARTIFACTS_DIR.iterdir() if p.is_file()]

    user = render_prompt("self_check.j2",
        rubric_json=json.dumps(rubric.model_dump(), ensure_ascii=False),
        artifacts=sorted(artifacts),
        haupttext_excerpt=_read_excerpt(config.ARTIFACTS_DIR / "03_va_hauptarbeit.md", 6000),
        konzept_excerpt=_read_excerpt(config.ARTIFACTS_DIR / "02_konzept.md", 3000),
        journal_excerpt=_read_excerpt(config.ARTIFACTS_DIR / "06_projektjournal.md", 3000),
        reflexion_excerpt=_read_excerpt(config.ARTIFACTS_DIR / "09_gesamtreflexion.md", 3000),
    )
    raw = await claude_opus_complete(system=SYSTEM, user=user, max_tokens=3500)
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
    report = json.loads(raw)

    atomic_write_json(config.OUTPUT_DIR / "score_report.json", report)
    await get_bus().emit(Event(type="score", data={"total": report["total"], "note": report["note"], "breakdown": report["teile"]}))

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"{report['total']}/120 Pkt = Note {report['note']}")
    log.info(f"[{NAME}] Score {report['total']}/120 in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=None, duration_s=duration), report
```

- [ ] **Step 3: Commit**

```bash
git add scripts/prompts/self_check.j2 scripts/subagents/self_check.py
git commit -m "feat: Self-Check-Subagent (120-Pt Rubrik-Bewertung)"
```

---

## Milestone 15: PDF-Render + ZIP-Bundle (30m · bis 02:40)

### Task 15.1: Haupttext-HTML-Template + Titelblatt

**Files:**
- Create: `templates/va_html.j2`
- Create: `templates/titelblatt_html.j2`

- [ ] **Step 1: va_html.j2 (für Haupttext mit Inhaltsverzeichnis)**

```jinja
<!DOCTYPE html>
<html lang="de">
<head><meta charset="utf-8"><title>{{ u.thema.titel }}</title>
<style>{{ css }}
.toc { margin: 1em 0; }
.toc ul { list-style: none; padding-left: 0; }
.toc li { padding-left: 1em; }
.figure { margin: 1em 0; text-align: center; page-break-inside: avoid; }
</style></head>
<body>

{# Titelblatt #}
<div style="page-break-after: always; text-align: center; padding-top: 6cm;">
<div style="font-size: 10pt;">Vertiefungsarbeit · Allgemeinbildender Unterricht · {{ u.schuelerin.schule }}</div>
<div style="font-size: 10pt; margin-top: 0.3cm;">Rahmenthema: <strong>{{ u.thema.rahmen }}</strong></div>
<h1 style="font-size: 24pt; margin-top: 4cm;">{{ u.thema.titel }}</h1>
<div style="font-size: 14pt; margin-top: 3cm;">{{ u.schuelerin.vorname }} {{ u.schuelerin.nachname }}</div>
<div style="font-size: 11pt;">{{ u.schuelerin.klasse }}</div>
<div style="font-size: 11pt; margin-top: 2cm;">Lehrperson: {{ u.schuelerin.lehrperson }}</div>
<div style="font-size: 11pt; margin-top: 0.2cm;">Abgabedatum: 15. April 2026</div>
</div>

{{ body_html | safe }}

</body></html>
```

- [ ] **Step 2: Commit**

```bash
git add templates/va_html.j2
git commit -m "feat: VA main HTML template with title page"
```

### Task 15.2: PDF-Bundle-Logik

**Files:**
- Modify: `scripts/media/pdf_render.py`

- [ ] **Step 1: Anonymize-Funktion und 3-Versionen-Render ergänzen**

Append to `scripts/media/pdf_render.py`:

```python
import re

def render_va_final(markdown: str, u: "Universe", out_main: Path, out_anonym: Path, out_gebunden: Path) -> None:
    """Rendert 3 VA-Versionen: vollständig / anonymisiert / gebunden (mit Bildern)."""
    import markdown as md_lib

    css = load_css()
    # 1. Hauptversion
    body_html = md_lib.markdown(markdown, extensions=["tables", "fenced_code", "toc"])
    tpl = _jinja.get_template("va_html.j2")
    html_main = tpl.render(body_html=body_html, css=css, u=u)
    out_main.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html_main, base_url=str(config.PROJECT_ROOT)).write_pdf(str(out_main))

    # 2. Anonymisierte Version (Wegleitung S. 19: "ohne Bilder, ohne Namen")
    anon_md = _anonymize(markdown, u)
    anon_html = md_lib.markdown(anon_md, extensions=["tables", "fenced_code", "toc"])
    # "ohne Bilder" — entferne <img>-Tags
    anon_html = re.sub(r"<img[^>]*>", "[Bild entfernt – anonymisierte Version]", anon_html)
    u_anon = u.model_copy(deep=True)
    u_anon.schuelerin.vorname = "***"
    u_anon.schuelerin.nachname = "***"
    html_anon = tpl.render(body_html=anon_html, css=css, u=u_anon)
    HTML(string=html_anon, base_url=str(config.PROJECT_ROOT)).write_pdf(str(out_anonym))

    # 3. Gebundene Version (identisch zu Haupt, nur Label)
    out_gebunden.write_bytes(out_main.read_bytes())


def _anonymize(md: str, u) -> str:
    out = md
    for name in [u.schuelerin.vorname, u.schuelerin.nachname,
                 f"{u.schuelerin.vorname} {u.schuelerin.nachname}",
                 u.interviewperson.name_anzeige,
                 "Dr. Weber", "Dr. phil. Andrea Weber",
                 u.schuelerin.lehrperson,
                 u.schuelerin.lehrbetrieb]:
        out = out.replace(name, "***")
    return out
```

- [ ] **Step 2: PDF-Bundle-Subagent (kein LLM, nur File-Ops)**

Create: `scripts/subagents/pdf_bundle.py`

```python
"""Finale PDF-Render + ZIP-Bundle. Kein LLM."""
from __future__ import annotations
import time
import zipfile
from pathlib import Path

from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import SubagentResult, emit_start, emit_done
from scripts.media.pdf_render import render_va_final
from scripts.utils import log

PHASE = 8
NAME = "pdf_bundle"

async def run(u: Universe, haupttext_md: str) -> SubagentResult:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    main_pdf = config.ARTIFACTS_DIR / "03_va_hauptarbeit.pdf"
    anon_pdf = config.ARTIFACTS_DIR / "04_va_hauptarbeit_anonym.pdf"
    geb_pdf = config.ARTIFACTS_DIR / "05_va_hauptarbeit_gebunden.pdf"
    render_va_final(haupttext_md, u, main_pdf, anon_pdf, geb_pdf)

    # ZIP-Bundle
    zip_path = config.OUTPUT_DIR / "va_komplett.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(config.ARTIFACTS_DIR.rglob("*")):
            if p.is_file():
                zf.write(p, arcname=p.relative_to(config.ARTIFACTS_DIR))

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"ZIP {zip_path.stat().st_size // 1024} KB")
    log.info(f"[{NAME}] Bundle fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=zip_path, duration_s=duration)
```

- [ ] **Step 3: Commit**

```bash
git add scripts/media/pdf_render.py scripts/subagents/pdf_bundle.py
git commit -m "feat: PDF-Bundle (3 VA-Versionen + ZIP)"
```

---

---

## Milestone 16: Orchestrator-Integration (45m · bis 03:25)

### Task 16.1: Voll-Orchestrator mit Phasen + Parallel-Fanout

**Files:**
- Modify: `scripts/orchestrator.py`

- [ ] **Step 1: Vollen Orchestrator schreiben**

```python
"""Phasen-Steuerung: 8 Phasen, Parallel-Fanout in P4."""
from __future__ import annotations
import asyncio
import time
from pathlib import Path

from scripts import config
from scripts.coherence import Universe, save_universe, load_universe
from scripts.event_bus import Event, get_bus
from scripts.rubric_parser import save_rubric_json
from scripts.utils import log

from scripts.subagents import (
    konzept, literatur, interview, audio, video, foto, umfrage,
    journal, reflexion, email, formular, praesentation,
    haupttext, redaktor, self_check, pdf_bundle,
)


async def emit_phase(phase: int, name: str, status: str = "running"):
    await get_bus().emit(Event(type="phase", data={"phase": phase, "name": name, "status": status}))


async def start_orchestrator(topic: str, rahmen: str) -> None:
    """Haupteinstieg — wird vom FastAPI-Endpoint POST /api/start getriggert."""
    if config.USE_PRERENDERED:
        await _replay_prerendered()
        return

    t_start = time.monotonic()
    try:
        # === Phase 1: Rubrik-Ingestion ===
        await emit_phase(1, "Rubrik-Ingestion")
        save_rubric_json()
        await emit_phase(1, "Rubrik-Ingestion", "done")

        # === Phase 2: Universum-Komposition ===
        await emit_phase(2, "Universum-Komposition")
        u = Universe.sample()
        u.thema.titel = topic
        u.thema.rahmen = rahmen
        save_universe(u)
        await emit_phase(2, "Universum-Komposition", "done")

        # === Phase 3: Konzept ===
        await emit_phase(3, "Konzept")
        await konzept.run(u)
        await emit_phase(3, "Konzept", "done")

        # === Phase 4: Parallel-Fanout ===
        await emit_phase(4, "Parallel-Fanout")

        # Runde 4a: unabhängige Tasks gleichzeitig starten
        literatur_task = asyncio.create_task(literatur.run(u))
        interview_task = asyncio.create_task(interview.run(u))
        umfrage_task = asyncio.create_task(umfrage.run(u))
        journal_task = asyncio.create_task(journal.run(u))
        reflexion_task = asyncio.create_task(reflexion.run(u))
        email_task = asyncio.create_task(email.run(u))
        formular_task = asyncio.create_task(formular.run(u))
        praesentation_task = asyncio.create_task(praesentation.run(u))
        foto_task = asyncio.create_task(foto.run(u))

        # Literatur blockiert Haupttext
        lit_result, quellen = await literatur_task
        u.quellen = quellen
        save_universe(u)

        # Interview blockiert Audio und Video
        int_result, transkript_md = await interview_task

        # Audio starten sobald Transkript da ist
        audio_task = asyncio.create_task(audio.run(u, transkript_md))

        # Foto braucht es für Video (Weber-Portrait)
        foto_result, foto_paths = await foto_task

        # Audio blockiert Video (Lip-Sync)
        audio_result = await audio_task

        # Video: braucht Foto + Audio
        video_task = asyncio.create_task(video.run(
            u,
            foto_paths.get("weber_portrait", config.ARTIFACTS_DIR / "foto_weber_portrait.png"),
            config.ARTIFACTS_DIR / "13_interview_audio.mp3",
        ))

        # Umfrage liefert Auswertungstext für Haupttext
        umfrage_result, umfrage_auswertung_md = await umfrage_task

        # Journal, Reflexion, E-Mail, Formular, Präsentation parallel fertigstellen
        await asyncio.gather(journal_task, reflexion_task, email_task, formular_task, praesentation_task, return_exceptions=True)

        # Video kann noch laufen — nicht auf ihn warten, wenn er zu langsam ist (Hedra kann >3 Min brauchen)
        # Wir geben ihm bis zum Ende der Phase 7 Zeit
        await emit_phase(4, "Parallel-Fanout", "done")

        # === Phase 5: Haupttext ===
        await emit_phase(5, "VA-Haupttext")
        haupttext_result, haupttext_md = await haupttext.run(u, transkript_md, umfrage_auswertung_md)
        await emit_phase(5, "VA-Haupttext", "done")

        # === Phase 6: Redaktor ===
        await emit_phase(6, "Redaktor-Pass")
        redaktor_result, redigiert_md = await redaktor.run(u, haupttext_md)
        await emit_phase(6, "Redaktor-Pass", "done")

        # === Phase 7: Self-Check ===
        await emit_phase(7, "Self-Check")
        check_result, report = await self_check.run(u)
        await emit_phase(7, "Self-Check", "done")

        # === Phase 8: PDF-Bundle ===
        await emit_phase(8, "PDF-Render & Bundle")
        # Video einsammeln (mit Timeout)
        try:
            await asyncio.wait_for(video_task, timeout=60)
        except (asyncio.TimeoutError, Exception) as e:
            log.warning(f"Video unfertig: {e}")

        await pdf_bundle.run(u, redigiert_md)
        await emit_phase(8, "PDF-Render & Bundle", "done")

        total_duration = time.monotonic() - t_start
        await get_bus().emit(Event(type="done", data={"duration_s": total_duration, "score": report["total"]}))
        log.info(f"✅ ORCHESTRATOR FERTIG in {total_duration/60:.1f} Min")

    except Exception as e:
        log.exception("Orchestrator crashed")
        await get_bus().emit(Event(type="error", data={"severity": "fatal", "message": str(e)}))
        raise


async def _replay_prerendered():
    """Pre-Rendered-Fallback: Artefakte aus prerendered/ nach artifacts/ kopieren, Events simulieren."""
    import shutil
    for f in config.PRERENDERED_DIR.iterdir():
        if f.is_file():
            shutil.copy(f, config.ARTIFACTS_DIR / f.name)
    # Simuliere Phasen-Verlauf mit Delays
    delays = [0.5, 0.8, 1.5, 6.0, 3.0, 1.0, 1.0, 0.8]
    for i, d in enumerate(delays, 1):
        await emit_phase(i, f"Phase {i} (Replay)")
        await asyncio.sleep(d)
        await emit_phase(i, f"Phase {i} (Replay)", "done")
    await get_bus().emit(Event(type="done", data={"duration_s": sum(delays), "replay": True}))
```

- [ ] **Step 2: Commit**

```bash
git add scripts/orchestrator.py
git commit -m "feat: full orchestrator with 8-phase pipeline + parallel fanout"
```

### Task 16.2: Server: Cost-Tracking + Artefakt-Listing erweitern

**Files:**
- Modify: `scripts/server.py`

- [ ] **Step 1: Cost-Tracker im Server aufnehmen (simpler Prozent-Estimator)**

Append in `scripts/server.py` after `_state = ...`:

```python
@app.get("/api/score")
async def api_score():
    import json
    from pathlib import Path
    p = config.OUTPUT_DIR / "score_report.json"
    if not p.exists():
        return {"ready": False}
    return {"ready": True, **json.loads(p.read_text(encoding="utf-8"))}
```

- [ ] **Step 2: Server hochfahren und Orchestrator triggern (Smoke-Test)**

```bash
# In einem Terminal:
uvicorn scripts.server:app --host 127.0.0.1 --port 8001 &

# Im anderen Terminal:
curl -X POST http://127.0.0.1:8001/api/start -H 'Content-Type: application/json' -d '{}'
# → {"ok": true}

# SSE-Stream anhören:
curl -N http://127.0.0.1:8001/api/stream
# → sollte "event: phase" Zeilen bringen
```

Expected: Phasen-Events kommen sichtbar rein. Artefakte erscheinen in `_output/agent/artifacts/` während der Ausführung.

- [ ] **Step 3: Commit**

```bash
git add scripts/server.py
git commit -m "feat: /api/score endpoint"
```

---

## Milestone 17: Frontend (60m · bis 04:25)

### Task 17.1: Frontend-Grundgerüst

**Files:**
- Modify: `scripts/web/index.html`
- Create: `scripts/web/app.js`
- Create: `scripts/web/style.css`

- [ ] **Step 1: index.html**

```html
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VA-Agent · ZAG PICTS Demo</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body>

<main id="app">

<!-- Screen A: Start -->
<section id="screen-start" class="screen active">
  <div class="card">
    <h1>🎓 VA-Agent · ZAG PICTS Demo</h1>
    <p class="subtitle">Eine komplette Vertiefungsarbeit in 20-25 Minuten.</p>

    <div class="fieldset">
      <label>Thema</label>
      <input id="topic" type="text" value="Einsamkeit im Alter — Wie Spitex-Fachleute sie erkennen und ihr begegnen">

      <label>Rahmenthema</label>
      <input id="rahmen" type="text" value="Gegensätze">
    </div>

    <div class="status">
      <div class="status-line">✅ Anthropic Claude Opus/Sonnet 4.6</div>
      <div class="status-line">✅ ElevenLabs v3 (Voice-Klon aktiv)</div>
      <div class="status-line">✅ Runway Gen-4 · Hedra Character-2 · FLUX 1.2 Pro</div>
      <div class="status-line">✅ OpenAlex · Google Books · PubMed · SRF</div>
    </div>

    <p class="meta">Erwartet: <strong>20-25 Minuten</strong> · <strong>~$40</strong></p>

    <button id="start-btn" class="primary">🚀  VA GENERIEREN</button>
  </div>
</section>

<!-- Screen B: Running -->
<section id="screen-running" class="screen">
  <div class="card wide">
    <header class="running-header">
      <div>
        <h2>🤖 Agent läuft</h2>
        <div id="elapsed">00:00</div>
      </div>
      <div class="progress-wrap">
        <div id="progress-bar"></div>
        <div id="progress-pct">0 %</div>
      </div>
    </header>

    <div class="two-cols">
      <div class="phases">
        <h3>Phasen</h3>
        <ol id="phase-list"></ol>
      </div>

      <div class="live-output">
        <h3>Live-Output</h3>
        <pre id="stream"></pre>
        <h3 style="margin-top: 1em;">Letzte Events</h3>
        <ul id="events"></ul>
      </div>
    </div>
  </div>
</section>

<!-- Screen C: Done -->
<section id="screen-done" class="screen">
  <div class="card wide">
    <header class="done-header">
      <h2>✅ VA fertig</h2>
      <div id="final-summary"></div>
    </header>

    <h3>Artefakte</h3>
    <div id="artifact-grid"></div>

    <div class="actions">
      <a id="zip-btn" class="primary" href="/api/zip" download>⬇  ALLES als ZIP</a>
    </div>

    <h3>Rubrik-Score · 120-Punkte-Raster nach Wegleitung</h3>
    <table id="rubric-table"></table>
  </div>
</section>

</main>

<script src="/static/app.js"></script>
</body>
</html>
```

- [ ] **Step 2: style.css (ZAG-Theme, dark)**

```css
:root {
  --magenta: #e30059;
  --lila: #7a00df;
  --bg: #0a0a0f;
  --card: #14141e;
  --fg: #f0f0f0;
  --muted: #888;
  --success: #3fc76b;
  --warn: #f5b242;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif; background: var(--bg); color: var(--fg); }
body { min-height: 100vh; display: flex; }
main#app { flex: 1; display: flex; align-items: center; justify-content: center; padding: 2em; }
.screen { display: none; width: 100%; max-width: 1200px; }
.screen.active { display: block; }
.card { background: var(--card); border: 1px solid #2a2a3a; border-radius: 8px; padding: 2em; box-shadow: 0 10px 40px rgba(0,0,0,0.4); }
.card.wide { max-width: none; }
h1 { color: var(--magenta); margin: 0 0 0.2em 0; font-size: 2em; }
h2 { color: var(--lila); margin: 0 0 0.5em 0; }
h3 { color: var(--magenta); margin: 1em 0 0.5em 0; font-size: 1.1em; }
.subtitle { color: var(--muted); margin: 0 0 1.5em 0; }
.fieldset { display: grid; gap: 0.6em; margin-bottom: 1.5em; }
label { font-size: 0.85em; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }
input { padding: 0.8em; background: #1f1f2e; color: var(--fg); border: 1px solid #2a2a3a; border-radius: 4px; font-size: 1em; }
.status { margin: 1em 0; font-size: 0.9em; }
.status-line { padding: 4px 0; color: var(--success); }
.meta { color: var(--muted); margin: 1em 0 1.5em 0; }
button.primary, a.primary { display: inline-block; padding: 1em 2em; background: var(--magenta); color: white; border: none; border-radius: 6px; font-size: 1.1em; font-weight: 600; cursor: pointer; text-decoration: none; transition: background 0.2s; }
button.primary:hover, a.primary:hover { background: var(--lila); }
.running-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2em; }
#elapsed { font-family: monospace; font-size: 1.2em; color: var(--muted); }
.progress-wrap { position: relative; width: 300px; height: 30px; background: #1f1f2e; border-radius: 4px; overflow: hidden; }
#progress-bar { height: 100%; width: 0; background: linear-gradient(90deg, var(--magenta), var(--lila)); transition: width 0.5s; }
#progress-pct { position: absolute; top: 0; left: 0; right: 0; bottom: 0; display: flex; align-items: center; justify-content: center; font-weight: 600; }
.two-cols { display: grid; grid-template-columns: 1fr 2fr; gap: 2em; }
.phases ol { list-style: none; padding: 0; }
.phases li { padding: 0.4em 0; border-bottom: 1px solid #2a2a3a; }
.phases li.running::before { content: "▶  "; color: var(--magenta); }
.phases li.done::before { content: "✅  "; }
.phases li.pending::before { content: "⋯  "; color: var(--muted); }
.phases li.running { color: var(--fg); font-weight: 600; }
.phases li.pending { color: var(--muted); }
.live-output pre { background: #1f1f2e; padding: 1em; border-radius: 4px; max-height: 300px; overflow-y: auto; font-size: 0.85em; white-space: pre-wrap; }
.live-output ul { list-style: none; padding: 0; font-family: monospace; font-size: 0.85em; max-height: 200px; overflow-y: auto; }
.live-output li { padding: 2px 0; }
#artifact-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 0.5em; margin: 1em 0; }
.artifact { padding: 0.8em; background: #1f1f2e; border-radius: 4px; display: flex; justify-content: space-between; align-items: center; }
.artifact a { color: var(--magenta); text-decoration: none; margin-left: 1em; }
.artifact a:hover { color: var(--lila); }
.actions { margin: 2em 0; text-align: center; }
#rubric-table { width: 100%; border-collapse: collapse; margin-top: 1em; }
#rubric-table th, #rubric-table td { padding: 0.6em; border-bottom: 1px solid #2a2a3a; text-align: left; }
#rubric-table .total { font-weight: 700; color: var(--magenta); }
#final-summary { color: var(--muted); margin-top: 0.5em; }
```

- [ ] **Step 3: app.js**

```javascript
const PHASES = [
  {n:1, name:"Rubrik-Ingestion"},
  {n:2, name:"Universum-Komposition"},
  {n:3, name:"Konzept"},
  {n:4, name:"Parallel-Fanout (11 Subagenten)"},
  {n:5, name:"VA-Haupttext"},
  {n:6, name:"Redaktor-Pass"},
  {n:7, name:"Rubrik-Self-Check"},
  {n:8, name:"PDF-Render & Bundle"},
];

const screens = {
  start: document.getElementById("screen-start"),
  running: document.getElementById("screen-running"),
  done: document.getElementById("screen-done"),
};
function show(name) {
  Object.values(screens).forEach(s => s.classList.remove("active"));
  screens[name].classList.add("active");
}

const startBtn = document.getElementById("start-btn");
const topicInput = document.getElementById("topic");
const rahmenInput = document.getElementById("rahmen");
const phaseList = document.getElementById("phase-list");
const streamEl = document.getElementById("stream");
const eventsEl = document.getElementById("events");
const elapsedEl = document.getElementById("elapsed");
const progressBar = document.getElementById("progress-bar");
const progressPct = document.getElementById("progress-pct");
const finalSummary = document.getElementById("final-summary");
const artifactGrid = document.getElementById("artifact-grid");
const rubricTable = document.getElementById("rubric-table");

function renderPhases(currentPhase, phaseStatus) {
  phaseList.innerHTML = PHASES.map(p => {
    const cls = phaseStatus[p.n] === "done" ? "done"
             : (p.n === currentPhase ? "running" : "pending");
    return `<li class="${cls}" data-phase="${p.n}">${p.n}  ${p.name}</li>`;
  }).join("");
}

let startTs = null;
function tickElapsed() {
  if (!startTs) return;
  const s = Math.floor((Date.now() - startTs) / 1000);
  const m = String(Math.floor(s/60)).padStart(2, "0");
  const sec = String(s%60).padStart(2, "0");
  elapsedEl.textContent = `${m}:${sec}`;
}
setInterval(tickElapsed, 1000);

startBtn.addEventListener("click", async () => {
  startTs = Date.now();
  show("running");
  renderPhases(1, {});
  const body = { topic: topicInput.value, rahmen: rahmenInput.value };
  await fetch("/api/start", { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body) });
  const es = new EventSource("/api/stream");
  const phaseStatus = {};
  es.addEventListener("phase", e => {
    const d = JSON.parse(e.data).data;
    if (d.status === "done") phaseStatus[d.phase] = "done";
    const currentPhase = d.phase + (d.status === "done" ? 1 : 0);
    renderPhases(Math.min(currentPhase, 8), phaseStatus);
    const pct = Math.round((Object.keys(phaseStatus).length / 8) * 100);
    progressBar.style.width = pct + "%";
    progressPct.textContent = pct + " %";
    addEvent(`Phase ${d.phase} · ${d.name} · ${d.status}`);
  });
  es.addEventListener("subtask", e => {
    const d = JSON.parse(e.data).data;
    addEvent(`  └ ${d.task}: ${d.status} ${d.detail || ""}`);
  });
  es.addEventListener("stream", e => {
    const d = JSON.parse(e.data).data;
    streamEl.textContent += d.delta;
    streamEl.scrollTop = streamEl.scrollHeight;
  });
  es.addEventListener("error", e => {
    try { const d = JSON.parse(e.data).data; addEvent(`⚠️ ${d.task || ""}: ${d.message}`); } catch {}
  });
  es.addEventListener("done", async e => {
    es.close();
    await renderDone();
  });
});

function addEvent(text) {
  const li = document.createElement("li");
  const time = new Date().toLocaleTimeString();
  li.textContent = `${time}  ${text}`;
  eventsEl.insertBefore(li, eventsEl.firstChild);
  while (eventsEl.childElementCount > 40) eventsEl.removeChild(eventsEl.lastChild);
}

async function renderDone() {
  const [artifacts, score] = await Promise.all([
    fetch("/api/artifacts").then(r => r.json()),
    fetch("/api/score").then(r => r.json()),
  ]);
  const totalS = Math.floor((Date.now() - startTs) / 1000);
  finalSummary.textContent = `${Math.floor(totalS/60)}:${String(totalS%60).padStart(2,"0")} Min · ${artifacts.length} Artefakte`;
  artifactGrid.innerHTML = artifacts.map(a => `
    <div class="artifact">
      <span>${a.filename} <small>(${Math.round(a.size/1024)} KB)</small></span>
      <span><a href="/api/artifacts/${encodeURIComponent(a.filename)}" target="_blank">Öffnen</a>
           <a href="/api/artifacts/${encodeURIComponent(a.filename)}" download>↓</a></span>
    </div>
  `).join("");

  if (score.ready) {
    rubricTable.innerHTML = `
      <tr><th>Teil</th><th>Score</th></tr>
      <tr><td>A · Prozess</td><td>${score.teile.A_prozess.score} / 30</td></tr>
      <tr><td>B · Produkt</td><td>${score.teile.B_produkt.score} / 50</td></tr>
      <tr><td>C · Präsentation</td><td>${score.teile.C_praesentation.score} / 40</td></tr>
      <tr class="total"><td>Total</td><td>${score.total} / 120 = Note ${score.note}</td></tr>
    `;
  }
  show("done");
}
```

- [ ] **Step 4: Smoke-Test im Browser**

```bash
uvicorn scripts.server:app --host 127.0.0.1 --port 8001 &
open http://127.0.0.1:8001/
```

Erwartet: Screen A lädt, Button klickbar.

- [ ] **Step 5: Commit**

```bash
git add scripts/web/
git commit -m "feat: three-screen frontend with SSE dashboard"
```

---

## Milestone 18: End-to-End Dry-Run 1 + Fixes (60m · bis 05:25)

### Task 18.1: Vollständiger Dry-Run

- [ ] **Step 1: Artifacts & Output-Verzeichnis leeren**

```bash
rm -rf _output/agent/artifacts/* _output/agent/*.json _output/agent/*.zip
```

- [ ] **Step 2: Server starten und triggern**

```bash
uvicorn scripts.server:app --host 127.0.0.1 --port 8001 &
open http://127.0.0.1:8001/
# Im Browser: Topic übernehmen, Start klicken.
```

- [ ] **Step 3: Log-Stream beobachten**

Parallel in einem zweiten Terminal:
```bash
tail -f /tmp/va-agent-debug.log 2>/dev/null || true
# Alternativ: rich logs erscheinen direkt in dem Terminal wo uvicorn läuft
```

- [ ] **Step 4: Prüf-Matrix am Ende**

Erwartete Artefakte (18-20 Dateien):

```bash
ls -la _output/agent/artifacts/
```

Pflicht:
- [ ] `02_konzept.pdf` vorhanden, 3-5 Seiten
- [ ] `03_va_hauptarbeit.pdf` vorhanden, 10-18 Seiten
- [ ] `04_va_hauptarbeit_anonym.pdf` vorhanden, Namen `***`
- [ ] `05_va_hauptarbeit_gebunden.pdf` vorhanden
- [ ] `06_projektjournal.pdf` vorhanden, 8 Wochen
- [ ] `07_zwischenreflexion_1.pdf` + `08_zwischenreflexion_2.pdf`
- [ ] `09_gesamtreflexion.pdf`
- [ ] `10_eigenstaendigkeitserklaerung.pdf` + `11_einverstaendniserklaerung_interview.pdf`
- [ ] `12_interview_transkript.pdf` + `13_interview_audio.mp3` (abspielbar)
- [ ] `14_interview_video_lipsync.mp4` (evtl. fehlt bei Hedra-Timeout)
- [ ] `15_umfrage_fragebogen.pdf` + `16_umfrage_rohdaten.csv` + 5 Plots
- [ ] `17_video_broll.mp4` (evtl. fehlt bei Runway-Timeout)
- [ ] `18_zwischenpraesentation.pptx` + `19_schlusspraesentation.pptx`
- [ ] `20_emails/` mit 7 `.eml`
- [ ] `score_report.json` mit Total ≥ 80

- [ ] **Step 5: Wenn ein Subagent crasht**

Pattern: Logs lesen → Prompt-Output inspizieren → Prompt präzisieren → erneut ausführen (nur jener Subagent via `scripts/dev_test_<name>.py`, wenn vorhanden).

Häufige Probleme:
- **JSON-Parse fehlschlägt**: Prompt expliziter machen, "Gib reines JSON, keine Fences zurück"
- **Markdown-Render bricht**: Sonderzeichen escapen, `escape` in Jinja-Template
- **WeasyPrint fehler**: CSS-Prüfung, `base_url` korrekt
- **ElevenLabs 429**: Rate-Limit, Pause zwischen Turns einbauen (z.B. `await asyncio.sleep(0.5)`)
- **Runway/Hedra Timeout**: Fallback-Block in video.py robust
- **FLUX NSFW-Filter**: Prompts harmloser formulieren

- [ ] **Step 6: Commit der Fixes**

```bash
git add -A
git commit -m "fix: dry-run 1 corrections"
```

### Task 18.2: Koherenz-Check

- [ ] **Step 1: Koherenz-Check-Skript**

Create: `scripts/dev_coherence_check.py`

```python
"""Post-Hoc: geht durch alle Markdown-Artefakte und meldet Inkonsistenzen."""
from pathlib import Path
from scripts.coherence import load_universe, validate_artifact_text
from scripts import config

u = load_universe()
total_issues = []
for f in config.ARTIFACTS_DIR.rglob("*.md"):
    text = f.read_text(encoding="utf-8")
    issues = validate_artifact_text(f.name, text, u)
    total_issues.extend(issues)

if total_issues:
    print(f"⚠ {len(total_issues)} Koherenz-Probleme:")
    for i in total_issues:
        print(f"  • {i}")
else:
    print("✅ Keine Koherenz-Probleme gefunden")
```

```bash
python scripts/dev_coherence_check.py
```

Expected: "Keine Koherenz-Probleme" oder Liste kurzer Fixes.

- [ ] **Step 2: Commit**

```bash
git add scripts/dev_coherence_check.py
git commit -m "tooling: coherence check script"
```

---

## Milestone 19: Pre-Rendered-Fallback (30m · bis 05:55)

### Task 19.1: Artefakte sichern

- [ ] **Step 1: Aktuelle Artefakte als Pre-Rendered kopieren**

```bash
cp -r _output/agent/artifacts/* _output/agent/prerendered/
cp _output/agent/score_report.json _output/agent/prerendered/score_report.json
```

- [ ] **Step 2: Fallback testen**

Edit `.env`: `USE_PRERENDERED=1`

```bash
# Artifacts löschen, dann server neu starten
rm -rf _output/agent/artifacts/*
uvicorn scripts.server:app --host 127.0.0.1 --port 8001 &
# Browser: http://127.0.0.1:8001/ → Start
```

Expected: SSE-Events laufen mit simulierten Delays, am Ende sind Artefakte wieder in `artifacts/` (via `_replay_prerendered()`).

- [ ] **Step 3: Wieder Live-Modus**

Edit `.env`: `USE_PRERENDERED=0`

- [ ] **Step 4: Commit**

```bash
git add _output/agent/prerendered/ # falls nicht gitignored
# ACHTUNG: prerendered Artefakte können gross sein. Nur committen wenn .gitignore NICHT _output/agent/* hat.
# Alternativ lokal behalten.
```

---

## Milestone 20: Dry-Run 2 + Polish + Sleep-Buffer (90m · bis 07:25)

### Task 20.1: Zweiter End-to-End Dry-Run

- [ ] **Step 1: Frische Artifacts-Dir**

```bash
rm -rf _output/agent/artifacts/*
rm -f _output/agent/score_report.json _output/agent/va_komplett.zip
```

- [ ] **Step 2: Server starten, in Browser triggern**

```bash
uvicorn scripts.server:app --host 127.0.0.1 --port 8001
# Browser → Start
```

Beobachte:
- Timing pro Phase
- Progress-Bar bewegt sich
- Live-Stream zeigt Haupttext-Tokens
- Keine Fehler im Terminal

- [ ] **Step 3: Exit-Kriterien prüfen (harte Gates)**

Alle müssen JA sein:
- [ ] ≥ 16 Artefakte im Grid (ideal 18+)
- [ ] VA-PDF öffnet in Browser/Preview, zeigt 10-15 Seiten
- [ ] Audio spielt ab, zwei Stimmen unterscheidbar
- [ ] Score ≥ 80/120
- [ ] ZIP-Download funktioniert und entpackt sauber
- [ ] Gesamtlaufzeit ≤ 25 Min
- [ ] Kein Crash in der uvicorn-Konsole

Falls NEIN: entweder Fix oder Pre-Rendered-Modus aktivieren.

### Task 20.2: Visual Polish

- [ ] **Step 1: Hübschere Artefakt-Icons im Grid**

Edit `scripts/web/app.js`:

Mapping-Funktion ergänzen:
```javascript
function iconFor(filename) {
  if (filename.endsWith(".pdf")) return "📄";
  if (filename.endsWith(".mp3")) return "🎵";
  if (filename.endsWith(".mp4")) return "🎬";
  if (filename.endsWith(".png") || filename.endsWith(".jpg")) return "🖼";
  if (filename.endsWith(".csv")) return "📊";
  if (filename.endsWith(".pptx")) return "💻";
  if (filename.endsWith(".eml")) return "📧";
  if (filename.endsWith(".md")) return "📝";
  return "📎";
}
// In renderDone, im template-literal:
// `<span>${iconFor(a.filename)} ${a.filename}...`
```

- [ ] **Step 2: Final-Screen-Überschrift mit Dramatik**

In `renderDone()`:

```javascript
finalSummary.innerHTML = `<strong>${Math.floor(totalS/60)}:${String(totalS%60).padStart(2,"0")} Min</strong> · ${artifacts.length} Artefakte · Score <strong>${score.total}/120</strong> · <strong>Note ${score.note}</strong>`;
```

- [ ] **Step 3: Commit**

```bash
git add scripts/web/app.js
git commit -m "polish: artifact icons, final summary emphasis"
```

### Task 20.3: Cheat-Sheet für den Talk

- [ ] **Step 1: Create `scripts/TALK_CHEATSHEET.md`** (nicht committed, nur persönlich)

```markdown
# Morgen 17.04. Ablauf

## 07:00 Aufstehen
- Laptop laden (mind. 80 %)
- 5G-Hotspot laden

## 07:30 Im Saal
- Beamer HDMI
- Auflösung 1280×720
- Browser Vollbild
- URL: http://127.0.0.1:8001/

## 08:00 Agent starten
Terminal 1:
  cd ~/Desktop/Coding/picts_input
  source .venv/bin/activate
  uvicorn scripts.server:app --host 127.0.0.1 --port 8001
Browser:
  http://127.0.0.1:8001/ → Start

## 08:00-08:25 Referat läuft parallel
Agent ist im Hintergrund-Tab offen. Zurück schalten wenn gewünscht.

## 08:25 Reveal
"Ich habe um 8:00 einen Agenten gestartet. Der läuft jetzt."
Browser-Tab wechseln.
Durch Artefakte klicken.

## Fallback
USE_PRERENDERED=1 in .env setzen, Server neu starten.

## Post-Talk (ab 09:00)
- ElevenLabs Voice-ID löschen
- Browser-Fenster mit erfundenen Daten schliessen
- Laptop sperren
```

- [ ] **Step 2: Mindestens 3 Stunden Schlaf einplanen**

Wenn wir jetzt 05:55 sind, heisst das: spätestens 07:00 aufhören. Sleep-Buffer = 1 Stunde Schlaf, bevor Generalprobe um 07:30.

Wenn 05:00 erreicht ist: 2 Stunden Schlaf möglich.

---

## Self-Review-Checkliste (nach Plan-Fertigstellung, nicht ausführen, nur prüfen)

### 1. Spec-Coverage

Jeder Spec-Abschnitt hat eine Task-Zuordnung:

| Spec-§ | Plan-Task |
|---|---|
| §0 Kernziel / fixfertige VA | alle Milestones, insbes. M15 (PDF-Bundle) |
| §1 Standalone-Web-App (3 Screens) | M2 (FastAPI-Skeleton), M17 (Frontend) |
| §3 Architektur | M2 (Server), M16 (Orchestrator) |
| §4 Fiktiv-Universum | M4 (Coherence + Universe) |
| §5-6 Phasen + Subagenten | M5 (Rubric), M6-M14 (je Subagent), M16 (Wiring) |
| §7 Web-App-UI | M17 |
| §8 Stimmklon | M3 |
| §10 Rubrik-Optimierung | M5, M14.3 (Self-Check) |
| §11 Fehlerbehandlung | `utils.retry_async` in M1.4, `_safe` in M9 video |
| §12 Pre-Rendered-Fallback | M19 |
| §13 Ethik | nicht in Code — Ramon-Verantwortung (consent = er selbst) |
| §14 Dry-Run-Plan | M18, M20 |
| §17 Offene Entscheidungen | Defaults in `config.py` (M1.4) + Universe.sample() (M4) |

Keine Spec-Lücken.

### 2. Placeholder-Scan

Durchsuche nach `TODO`, `TBD`, "...", "implementiere später". Alle Code-Blöcke sind komplett. ✅

### 3. Type-Konsistenz

- `Universe`, `Schuelerin`, `Interviewperson` konsistent verwendet
- `SubagentResult` in allen Subagenten retourniert
- `Event`-Typen im SSE-Stream: `phase`, `subtask`, `stream`, `score`, `done`, `error` — konsistent im Frontend
- `.env`-Keys gleich in `config.py` und `.env.example` ✅

### 4. Zeitbudget realistisch?

M1-M5 (Setup + Foundation): 2h 20min → bis 20:20
M6-M14 (Subagenten): 5h 15min → bis 01:35 (Buffer 0:25)
M15-M17 (Bundle + UI): 2h → bis 04:25 (Buffer 0:10)
M18-M19 (Dry-Run + Fallback): 1h 30min → bis 05:55
M20 (Polish + Sleep): bis 07:25

**Brauchbar, wenn keine unerwarteten API-Probleme auftreten.** Wenn Video-APIs scheitern (wahrscheinlich!), ist der Fallback auf Stock/Platzhalter wichtig, um Zeit zu gewinnen.

---

**Plan-Ende. Gesamtlänge: 20 Milestones, 58 Tasks, ~5000 LoC in 13 Stunden.**

