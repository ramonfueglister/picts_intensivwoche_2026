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

        # Audio blockiert Video (Lip-Sync) — graceful degrade wenn ElevenLabs fails
        try:
            audio_result = await audio_task
        except Exception as e:
            log.warning(f"Audio-Agent failed ({e}), Video-LipSync wird übersprungen")
            await get_bus().emit(Event(type="error", data={"severity": "warn", "task": "audio", "message": str(e)}))
            audio_result = None

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
