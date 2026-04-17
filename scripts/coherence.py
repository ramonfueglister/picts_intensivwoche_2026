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
