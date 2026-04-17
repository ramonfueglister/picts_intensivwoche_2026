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
