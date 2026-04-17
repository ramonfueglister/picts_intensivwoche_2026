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
