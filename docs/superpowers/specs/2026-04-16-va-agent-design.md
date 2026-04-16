# Design-Spec — VA-Agent (Standalone-Web-App)

**Version** 2 · Refokus nach Gespräch 2026-04-16 22:00
**Anlass** PICTS-Woche Grundbildung · Freitag, 17.04.2026 · ZAG Winterthur
**Autor** Ramon Füglister
**Entstehung** Brainstorming-Session 2026-04-16

---

## 0. Kernziel — nicht aus den Augen verlieren

**Am Ende des 30-Min-Slots existiert eine fixfertige, vollständige Vertiefungsarbeit.** Das ist das einzige Ziel, das zählt. Alles andere (Ticker, Encores, Live-Show) ist nachrangig und darf dieses Ziel nie gefährden.

Fixfertig heisst:
- VA-Hauptarbeit als PDF, 10-15 Seiten, Arial 11, Zeilenabstand 1.5, Wegleitung-konform
- Alle Pflicht-Beilagen (Konzept, Projektjournal, 2 Zwischenreflexionen, Gesamtreflexion, Eigenständigkeitserklärung, Einverständniserklärung)
- Alle eigenständigen Methoden-Artefakte (Interview mit Audio, Umfrage mit Daten+Plots, B-Roll-Video, Fotos)
- Alle Präsentations-Artefakte (Zwischen- und Schlusspräsentation .pptx + Sprechnotizen)
- Alle Nebenprodukte (6-8 E-Mail-Drafts, Fake-Unterschriften)
- Download-bar als ZIP

---

## 1. Form — Standalone-Web-App im Browser

Eine separate Web-App, die auf `http://localhost:8001` läuft. Am Rednerpult zieht Ramon die URL auf den Beamer (oder zeigt sie als zweiter Tab), klickt **Start**, und die App rattert alles runter. Das Publikum sieht live, was passiert: Phasen schalten weiter, Live-Text streamt aus dem Interview-Agent, Fortschrittsbalken wächst.

**Drei Screens:**

### 1.1 Screen A — Start

```
┌───────────────────────────────────────────────────────────────┐
│  🎓 VA-Agent · ZAG PICTS Demo                                 │
│  ─────────────────────────────────────────────────────────    │
│                                                                │
│   Thema:           [Einsamkeit im Alter — Spitex-Perspektive] │
│   VA-Rahmenthema:  [Gegensätze]                               │
│                                                                │
│   Fiktive:r Lernende:r:                                       │
│   Name:            [Luca Brunner]                             │
│   Klasse:          [FaGe 24b]                                 │
│   Lehrbetrieb:     [Spitex Zürich Limmat]                     │
│                                                                │
│   API-Status:                                                  │
│   ✅ Anthropic Claude                                          │
│   ✅ ElevenLabs (inkl. geklonte Stimme "Ramon→Luca")           │
│   ✅ Runway Gen-4 · Hedra Character-2 · FLUX 1.2 Pro           │
│   ✅ OpenAlex · Google Books · PubMed                          │
│                                                                │
│   Erwartete Dauer: 20-25 Min · Erwartete Kosten: ~$40          │
│                                                                │
│   [         🚀  VA GENERIEREN         ]                        │
└───────────────────────────────────────────────────────────────┘
```

### 1.2 Screen B — Running

```
┌───────────────────────────────────────────────────────────────┐
│  🤖 Agent läuft · 04:23 / ~22:00 · $12.40 bisher              │
│  ▓▓▓▓▓▓░░░░░░░░░░░░░░░░░  21 %                                │
│  ─────────────────────────────────────────────────────────    │
│                                                                │
│  Phasen                                                        │
│   ✅ 1  Rubrik-Ingestion                          14s          │
│   ✅ 2  Universum-Komposition                     58s          │
│   ✅ 3  Konzept                                   82s  9/9 P   │
│   ▶  4  Parallel-Fanout (8 Subagenten)                         │
│        ├ ✅ Literatur-Recherche     12 Quellen                 │
│        ├ ▶  Interview-Skript        Claude streamt…            │
│        ├ ▶  Audio-Synthese          ElevenLabs queue 2/8       │
│        ├ ▶  Video-Generation        Runway ~90s                │
│        ├ ▶  Foto-Agent              FLUX 3/5                    │
│        ├ ⋯  Umfrage                                            │
│        ├ ⋯  Journal                                            │
│        ├ ⋯  Reflexionen                                        │
│        ├ ⋯  E-Mails                                            │
│        ├ ⋯  Formulare                                          │
│        └ ⋯  Präsentationen                                     │
│   ⋯ 5  VA-Haupttext (wartet auf 4a/4b/4c)                     │
│   ⋯ 6  Redaktor-Pass                                          │
│   ⋯ 7  Rubrik-Self-Check                                      │
│   ⋯ 8  PDF-Render & Bundle                                    │
│                                                                │
│  Live-Output (Interview-Agent streamt)                        │
│  ┌───────────────────────────────────────────────────────┐    │
│  │ Dr. Weber: "Einsamkeit ist bei unseren Spitex-Klient:innen│
│  │ eigentlich ein täglicher Begleiter. Besonders bei den  │    │
│  │ Alleinlebenden merken wir, wie wichtig jeder Besuch    │    │
│  │ ist — manchmal sind wir die einzigen Menschen, die     │    │
│  │ ▊                                                       │    │
│  └───────────────────────────────────────────────────────┘    │
│                                                                │
│  Letzte Events                                                 │
│  22:23:14  ✅ Literatur: 12 Quellen, davon 4 CH-Medien         │
│  22:23:01  ✅ Konzept: 9/9 Punkte (Self-Check bestanden)       │
│  22:22:38  ▶  Parallel-Fanout gestartet (8 Tasks)              │
└───────────────────────────────────────────────────────────────┘
```

### 1.3 Screen C — Done

```
┌───────────────────────────────────────────────────────────────┐
│  ✅ VA fertig · 22:17 min · $41.80 · 91/120 Punkte (Note 5.0)  │
│  ─────────────────────────────────────────────────────────    │
│                                                                │
│  18 Artefakte                                                  │
│                                                                │
│   📄  Titelblatt                              [Öffnen] [↓]    │
│   📄  VA-Konzept  (3 S.)                      [Öffnen] [↓]    │
│   📄  VA-Hauptarbeit  (14 S.)                 [Öffnen] [↓]    │
│   📄  VA-Hauptarbeit (anonymisiert)           [Öffnen] [↓]    │
│   📄  VA-Hauptarbeit (gebunden, Druckversion) [Öffnen] [↓]    │
│   📄  Projektjournal  (8 Wochen, 12 S.)       [Öffnen] [↓]    │
│   📄  Zwischenreflexion 1 + 2                 [Öffnen] [↓]    │
│   📄  Gesamtreflexion                         [Öffnen] [↓]    │
│   📄  Eigenständigkeitserklärung              [Öffnen] [↓]    │
│   📄  Einverständniserklärung Interview       [Öffnen] [↓]    │
│   📄  Interview-Transkript  (7 S.)            [Öffnen] [↓]    │
│   🎵  Interview-Audio.mp3  (7:42)             [▶ Play]  [↓]   │
│   🎬  Interview-Video (Lip-Sync, 22s)         [▶ Play]  [↓]   │
│   📄  Umfrage-Fragebogen                      [Öffnen] [↓]    │
│   📊  Umfrage-Rohdaten + 5 Plots              [Öffnen] [↓]    │
│   🎬  B-Roll-Video (6s)                       [▶ Play]  [↓]   │
│   🖼  Fotos (5 Stück)                         [Galerie] [↓]   │
│   💻  Zwischenpräsentation.pptx               [Öffnen] [↓]    │
│   💻  Schlusspräsentation.pptx + Sprechnotizen[Öffnen] [↓]    │
│   📧  E-Mail-Drafts (7)                       [Öffnen] [↓]    │
│                                                                │
│   [  ⬇  ALLES als ZIP (142 MB)  ]                             │
│                                                                │
│  Rubrik-Score (120-Punkte-Matrix nach Wegleitung S. 23-25)    │
│   Teil A Prozess            24 / 30                           │
│     Konzept                  9 / 9                            │
│     Projektjournal           6 / 6                            │
│     Reflexion                6 / 6                            │
│     Zwischenpräsentation     3 / 6  ⚠ nur Slides, kein Vortrag│
│     Lehrperson               0 / 3  ⚠ nicht automatisierbar   │
│   Teil B Produkt            50 / 50                           │
│   Teil C Präsentation       17 / 40  ⚠ Vortrag nicht gen.     │
│   ────────────────────────────                                │
│   Total                     91 / 120  =  Note 5.0              │
└───────────────────────────────────────────────────────────────┘
```

---

## 2. Scope

### 2.1 In Scope

- Python-Backend (FastAPI) + Vanilla-JS-Frontend, alles als Single-Page-App
- 8-phasiger Agent-Orchestrator mit parallelem Fan-Out in Phase 4
- 18 Artefakte (siehe Screen C oben), jedes als einzeln downloadbare Datei + als ZIP
- Rubrik-getriebene Self-Optimization gegen das 120-Punkte-Raster
- Multi-Doc-Kohärenz via `universe.json` (Single Source of Truth)
- Stimmklon Ramons → Lernende:r "Luca" (ElevenLabs Professional Voice Cloning)
- Lip-Sync-Video der fiktiven Interviewperson via Hedra Character-2
- Pre-Rendered-Fallback (heute Abend einmal durchgelaufen, als "Safety Net" auf dem Laptop)

### 2.2 Out of Scope

- Keine Integration in `slides.qmd` / reveal.js (App läuft komplett separat)
- Keine Publikation/Hosting (läuft lokal auf Ramons MacBook)
- Kein Multi-User, kein Auth, keine Datenbank
- Kein Computer-Use (nicht Kernziel, zu fragil)
- Kein Avatar-Q&A (nicht Kernziel)
- Kein Live-Themen-Swap (nicht Kernziel)
- Keine Veröffentlichung der Artefakte nach dem Talk

Die drei Encore-Features aus V1 sind bewusst gestrichen. Falls nach dem Hauptlauf Diskussionszeit übrig bleibt, kann Ramon die fertige VA Seite für Seite durchgehen — das ist spektakulärer als jedes Encore, weil die Artefakte real vor einem liegen.

---

## 3. Architektur

```
┌─────────────────────────────────────────────────────────────┐
│  Browser (auf Beamer + lokal)                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  index.html + app.js (Vanilla JS, SSE-Client)         │  │
│  │   ├─ Screen A: Start                                   │  │
│  │   ├─ Screen B: Running (Live-Dashboard)                │  │
│  │   └─ Screen C: Done (Artefakte-Grid + Downloads)       │  │
│  └───────────────────────────────────────────────────────┘  │
│                       ▲ SSE ▼ HTTP                          │
└─────────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│  FastAPI @ localhost:8001                                    │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  GET  /                 → index.html                   │  │
│  │  GET  /app.js           → Frontend-Bundle              │  │
│  │  POST /start            → startet Orchestrator         │  │
│  │  GET  /stream           → SSE: Phasen + Events + Tokens│  │
│  │  GET  /artifacts/{id}   → einzelne Dateien             │  │
│  │  GET  /zip              → alle Artefakte als ZIP       │  │
│  │  GET  /score            → Rubrik-Score-Report          │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  scripts/orchestrator.py  (asyncio)                         │
│   ├─ Phase 1  Rubrik-Ingestion                              │
│   ├─ Phase 2  Universum-Komposition                         │
│   ├─ Phase 3  Konzept-Agent                                 │
│   ├─ Phase 4  Parallel-Fanout (asyncio.gather, 11 Tasks)    │
│   │    ├ Literatur · Interview · Audio · Video              │
│   │    ├ Foto · Umfrage · Journal · Reflexion               │
│   │    └ E-Mail · Formular · Präsentation                   │
│   ├─ Phase 5  VA-Haupttext (Streaming, wartet auf 4a+4b+4c) │
│   ├─ Phase 6  Redaktor-Pass                                 │
│   ├─ Phase 7  Rubrik-Self-Check                             │
│   └─ Phase 8  PDF-Render & ZIP-Bundle                       │
│                                                              │
│  Emit-Bus: jeder Subagent pusht Events auf Queue            │
│   → FastAPI streamt via SSE an Browser                      │
└──────────────────────────────────────────────────────────────┘
                            │
                            ▼
   _output/agent/
   ├─ status.json          (aktueller Zustand)
   ├─ universe.json        (Fiktiv-Universum, SSOT)
   ├─ rubric.json          (120-Punkte-Matrix, geparst aus PDF)
   ├─ score_report.json
   ├─ artifacts/           (18 Artefakte + ZIP)
   └─ prerendered/         (Fallback vom Vorabend)
```

---

## 4. Fiktiv-Universum (Single Source of Truth)

Vor jeder Artefakt-Generierung schreibt die Coherence-Manager-Komponente eine kanonische `universe.json`. Alle Subagenten lesen diese Datei und halten ihre Outputs konsistent.

### 4.1 Schema (gekürzt)

```jsonc
{
  "thema": {
    "rahmen": "Gegensätze",
    "titel": "Einsamkeit im Alter — Wie Spitex-Fachleute sie erkennen und ihr begegnen",
    "aspekte": ["Identität & Sozialisation", "Ethik", "Gender"],
    "methoden": ["Fachinterview", "Umfrage"]
  },
  "schuelerin": {
    "vorname": "Luca",
    "nachname": "Brunner",
    "pronomen": "er",
    "klasse": "FaGe 24b",
    "geburtsdatum": "2006-08-14",
    "lehrbetrieb": "Spitex Zürich Limmat, Standort Seefeld",
    "lehrperson": "Martina Keller",
    "schule": "ZAG Winterthur",
    "voice_id_elevenlabs": "ramon_cloned_YYYY",
    "schreibstil_marker": [
      "gelegentlich etwas lange Sätze",
      "verwendet gern 'eigentlich' und 'einfach'",
      "gendert konsequent mit Doppelpunkt",
      "ab und zu ein Rechtschreibfehler, den der Redaktor-Pass bewusst übersieht",
      "persönliche Anekdoten aus dem Praktikum"
    ]
  },
  "interviewperson": {
    "name_anzeige": "Dr. phil. Andrea Weber",
    "funktion": "Dozentin für Pflegewissenschaft, ZHAW Departement Gesundheit",
    "alter": 52,
    "email_fiktiv": "a.weber@example.ch",
    "foto_prompt": "50-jährige Pflegewissenschaftlerin, warme Ausstrahlung, Brille, kurze graumelierte Haare, helles Büro mit Bücherregal im Hintergrund",
    "tts_voice_id": "elevenlabs::preset::Elsa",
    "interview_termin": "2026-02-20",
    "urspruenglicher_termin_abgesagt": "2026-02-14"
  },
  "umfrage": {
    "plattform": "umfrageonline.ch",
    "url_anzeige": "https://umfrageonline.ch/s/luca-va-2026",
    "zeitraum": "2026-01-15 bis 2026-02-05",
    "n_versendet": 85,
    "n_ruecklauf": 52
  },
  "timeline": [
    { "woche": 1, "datum_start": "2025-12-01", "highlights": "Thema festgelegt, Mindmap",                  "journal_laenge": "normal" },
    { "woche": 4, "datum_start": "2025-12-22", "highlights": "Pause Weihnachten, Umfrage vorbereitet",      "journal_laenge": "kurz, gestresst" },
    { "woche": 5, "datum_start": "2026-01-12", "highlights": "Dr. Meier sagt ab",                            "journal_laenge": "frustriert" },
    { "woche": 6, "datum_start": "2026-01-19", "highlights": "Dr. Weber zugesagt",                           "journal_laenge": "erleichtert" }
  ],
  "quellen": [
    { "typ": "buch", "autor": "...", "titel": "...", "isbn": "...", "real_verified": true, "api_source": "google_books" }
  ],
  "konsistenz_regeln": [
    "Alle Daten in 2025/2026 (nicht vor 2025-12-01)",
    "Interviewpersonen-Name identisch in E-Mail + Transkript + Audio + Journal + Reflexion",
    "Voice-ID der Schülerstimme (Ramons Klon) konsistent über Interview-Audio hinweg",
    "Quellen im Quellenverzeichnis mit Kapitel-Zuordnung",
    "Mindestens 2 Quellen CH-spezifisch (SRF, BAG, Obsan, Pro Senectute)",
    "Projektjournal enthält Pannen: 1 Absage, 1 Weihnachtspause, 1 Self-Doubt-Eintrag"
  ]
}
```

### 4.2 Coherence Manager

`scripts/coherence.py`:
- `load_universe()` / `save_universe()` — atomare JSON-Writes
- `validate_artifact(path, universe)` — post-hoc Check auf Name/Datum-Konsistenz
- `generate_fake_signature(name, seed)` — deterministische SVG-Handschrift (Perlin-Noise), reproduzierbar für dieselbe Person

---

## 5. Phasen + Timing

Gesamt-Runtime: 20-25 Min.

| Phase | Dauer | Modus | Liefert |
|---|---|---|---|
| 1  Rubrik-Ingestion           | 20s    | seq      | `rubric.json` (120 Punkte + Kriterien) |
| 2  Universum-Komposition      | 60s    | seq      | `universe.json` |
| 3  Konzept                    | 90s    | seq      | `02_konzept.pdf` |
| 4  Parallel-Fanout (11 Tasks) | 10-16m | parallel | Artefakte 06–20 (ohne 03-05) |
| 5  VA-Haupttext (streaming)   | 4-6m   | seq      | `03_va_hauptarbeit.html` (Roh) |
| 6  Redaktor-Pass              | 2m     | seq      | Stil-vereinheitlichter Text |
| 7  Rubrik-Self-Check          | 2m     | seq      | `score_report.json` (+ ggf. Nachbesserung) |
| 8  PDF-Render & ZIP-Bundle    | 1m     | seq      | Finale PDFs + 3 Versionen + `all.zip` |

---

## 6. Subagenten

### 6.1 Konzept-Agent
- Modell: Claude Opus 4.6
- Input: `universe.thema`, `rubric.konzeptbeschrieb` (9 Punkte, 5 Kriterien)
- Output: `02_konzept.pdf` (2-3 Seiten)
- Pflichtstruktur: Themenbegründung (allg./persönlich/Wissenszuwachs), 3 Ziele mit je 2 ABU-Aspekten, 2 Methoden begründet, Zeitplan, Disposition
- Self-Check: 9/9 laut Rubrik, sonst Regenerierung

### 6.2 Literatur-Agent
- Modell: Claude Sonnet 4.6 + HTTP-Tools
- Tools: `search_openalex`, `search_google_books`, `search_pubmed`, `fetch_srf_article`
- Output: 8-12 reale Quellen in `universe.quellen` + paraphrasierbare Snippets
- Qualitätsregel: ≥ 1 Buch, ≥ 2 Fachartikel, ≥ 2 CH-Medien (SRF/BAG/Obsan/Pro Senectute), ≥ 1 Podcast/Doku

### 6.3 Interview-Agent
- Modell: Claude Opus 4.6
- Output: Frageleitfaden (12 Fragen) + Transkript (~2500 Wörter, 6-8 Min)
- Realismus-Regeln: 2-3 Fragen werden von Dr. Weber umformuliert/kritisiert, 1× längere Pause, 30s Thema-drift, konsistente Bio-Fakten

### 6.4 Audio-Agent
- Provider: ElevenLabs v3 Multilingual v2
- Stimmen: Luca = geklonte Ramon-Stimme, Dr. Weber = Preset "Elsa"
- Output: `13_interview_audio.mp3` (6-8 Min, stereo, 192 kbps)
- Post-Processing: leichte Raumakustik (FFmpeg-IR), Kaffeetasse 1× + Stuhl 1× als Hintergrundgeräusche, Normalisierung

### 6.5 Video-Agent (zwei parallele Tasks)
- **Task A — Lip-Sync-Interview-Clip**
  - Provider: Hedra Character-2
  - Input: Dr.-Weber-Foto (aus 6.6) + 20-Sek-Audio-Ausschnitt (aus 6.4)
  - Output: `14_interview_video_lipsync.mp4` (1080p, 20s)
- **Task B — B-Roll-Clip**
  - Provider: Runway Gen-4 Turbo (Fallback: Luma Ray-2)
  - Prompt: "Warme Spitex-Szene, Pflegende besucht ältere Person zuhause, Tageslicht, cinematic, dokumentarisch"
  - Output: `17_video_broll.mp4` (1080p, 6-8s)
  - Fallback: Pexels-Stock-Placeholder

### 6.6 Foto-Agent
- Provider: FLUX 1.2 Pro via fal-client
- 5 Bilder: Dr. Weber Headshot · Luca+Dr. Weber gemeinsam · Spitex-Situation · Einsamkeit-Symbolbild · Umfrage-Handzettel
- Naming/EXIF: iPhone 14, 2026-02-XX, Geo-Tag Zürich

### 6.7 Umfrage-Agent
- Output:
  - `15_umfrage_fragebogen.pdf` (wie umfrageonline-Export)
  - `16_umfrage_rohdaten.csv` (52 Zeilen, 18 Spalten, ~5 % Missing)
  - 5 Diagramme als PNG (Torte Demografie, 3 Balken, 1 Heatmap)
  - Auswertungstext ~800 Wörter für Haupttext
- Synthese-Regeln: Demografie laut `universe.umfrage`, innere Konsistenz (einsam ↔ wenig Kontakt), 12 CH-Umgangssprache-Zitate

### 6.8 Journal-Agent
- Modell: Claude Sonnet 4.6
- Output: `06_projektjournal.pdf` (8 Wocheneinträge)
- Pro Woche: Tätigkeiten/Dauer (5-8 Z.) + nächste Woche (3-5 Stichp.) + nächster Unterricht (1-2 Z.)
- Temporale Pannen: W4 kurz, W5 frustriert Absage, W6 erleichtert
- Schreibstil-Marker aus `universe.schuelerin.schreibstil_marker`

### 6.9 Reflexions-Agent
- Modell: Claude Sonnet 4.6
- Outputs:
  - `07_zwischenreflexion_1.pdf` (½ A4, Arial 10, LS 1.5, ~250 W.)
  - `08_zwischenreflexion_2.pdf` (½ A4, ~250 W.)
  - `09_gesamtreflexion.pdf` (¾ A4, ~400 W.)
- **Ironisches Kernelement** in Gesamtreflexion: Luca schreibt transparent, dass er ChatGPT für Rechtschreibkorrektur und Ideensuche benutzt habe. Meta-Lüge perfekt formuliert.

### 6.10 E-Mail-Agent
- Output-Format: `.eml` (RFC 5322, Draft-Zustand)
- 7 E-Mails: Anfrage Dr. Meier (wird abgelehnt), Absage-Mail (simulierter Empfang), Neu-Anfrage Dr. Weber, Zusage, Lehrperson-Zwischengespräch, Umfrage-Versand, Dank-Mail, Abgabe-Mail

### 6.11 Formular-Agent
- `10_eigenstaendigkeitserklaerung.pdf` (Wegleitung S. 20, exakter Wortlaut, "Luca Brunner"-Signatur)
- `11_einverstaendniserklaerung_interview.pdf` (Wegleitung S. 21, 4 Checkboxen, Dr.-Weber-Signatur)
- Signaturen via `generate_fake_signature()` (deterministisch, 2 Handschriftprofile)

### 6.12 Präsentations-Agent
- Claude Opus 4.6 + python-pptx
- `18_zwischenpraesentation.pptx` (5 Slides, 3-5 Min)
- `19_schlusspraesentation.pptx` (12 Slides, 10 Min) + `sprechnotizen.md` (3-6 Sätze pro Slide, Pausen-Hinweise, Moderationskärtchen)

### 6.13 VA-Haupttext-Agent
- Modell: Claude Opus 4.6 mit extended thinking
- Wartet auf: Literatur (6.2) + Interview (6.3) + Umfrage (6.7)
- Input: universe.json + alle Snippets
- Output: HTML-Entwurf (wird in Phase 8 zu PDF)
- Struktur: Titelblatt, Inhaltsverzeichnis, Einleitung (¾ S.), Haupttext 10-15 S. (4 Kapitel), Schlusswort (4-5 Sätze Zusammenfassung + ½ S. Kommentar), Quellenverzeichnis, Anhangsverweise
- Zitation: Interview mit "(Interview Dr. Weber, 20.02.2026)", Umfrage mit "(eigene Umfrage, N=52, Jan-Feb 2026)", Literatur APA-ähnlich

### 6.14 Redaktor-Agent
- Modell: Claude Sonnet 4.6
- Task: Stil-Vereinheitlichung auf FaGe-Lernenden-Niveau (nicht akademisch), Doppelpunkt-Gendern durchgängig, 1-2 bewusste kleine Stolperer behalten

### 6.15 Rubrik-Self-Check-Agent
- Modell: Claude Opus 4.6
- Input: `rubric.json` + alle finalen Artefakte
- Task: Punkte-Scoring pro Kriterium, bei Gesamt < 85 → identifiziere schwächste Kriterien, triggere max. 1 Regenerierungsrunde
- Output: `score_report.json` + `score_report.pdf` (wird in Screen C angezeigt)

---

## 7. Web-App-UI (FastAPI + Vanilla JS)

### 7.1 Endpoints

```
GET  /                    → index.html
GET  /app.js              → Frontend-Bundle (vanilla)
GET  /style.css           → Styling (ZAG-Theme übernehmen: Magenta #e30059, Lila #7a00df)
POST /start               → body: {topic?, rahmen?}; startet Orchestrator
GET  /stream              → text/event-stream: Phasen, Events, Tokens
GET  /artifacts           → JSON-Liste aller fertigen Artefakte
GET  /artifacts/{id}      → Datei-Download (oder inline-Preview)
GET  /zip                 → ZIP-Download aller Artefakte
GET  /score               → Rubrik-Score-Report als JSON
```

### 7.2 Frontend-Logik

Single-Page, drei Zustände (start/running/done), State-Switch via SSE-Events.

**SSE-Event-Typen:**
```jsonc
{"type": "phase",      "phase": 4, "name": "Parallel-Fanout", "status": "running"}
{"type": "subtask",    "phase": 4, "task": "literatur", "status": "done", "detail": "12 Quellen"}
{"type": "stream",     "phase": 5, "task": "haupttext", "delta": "Einsamkeit als..."}
{"type": "artifact",   "id": "13", "filename": "interview_audio.mp3", "ready": true}
{"type": "cost",       "amount_usd": 12.40}
{"type": "score",      "total": 91, "breakdown": {...}}
{"type": "done"}
{"type": "error",      "severity": "warn", "where": "video_agent", "message": "Runway timeout, Fallback"}
```

### 7.3 Styling

- ZAG-Farben aus `_extensions/zag-theme/zag.scss` übernehmen
- IBM Plex Sans (bereits im Projekt vorhanden)
- Dark mode (schwarzer Hintergrund, Magenta Akzente) — passt zum "Cognitive Surrender"-Slide-Kunstwerk
- Responsive bis 1280×720 (Beamer-Auflösung)

### 7.4 Resilience

- Wenn Client die SSE-Verbindung verliert: Reconnect + `?last_event=N` → Server schickt verpasste Events nach
- Wenn Backend crasht: Frontend zeigt "⚠ Verbindung verloren — läuft die App noch? (Terminal checken)"
- Keine Race Conditions durch single-writer: nur der Orchestrator schreibt in `status.json` und pusht SSE

---

## 8. Stimmklon (stark vereinfacht)

### 8.1 Subjekt: Ramon selbst

Weil du deine eigene Stimme gibst:
- Kein Dritt-Consent nötig
- Kein USB-Mikrofon-Setup am Freitagmorgen vor Ort
- Keine Ausfall-Risiken, wenn Kollegin absagt
- Aufnahme einmalig heute Abend, Voice-ID bleibt bis nach dem Talk

### 8.2 Ablauf (heute Abend)

1. **Aufnahme**: QuickTime oder Voice Memos, eingebautes MacBook-Mikrofon reicht für Instant Voice Cloning. Alternative: AirPods Pro.
2. **Dauer**: 90-120 Sekunden, neutraler Text (z.B. Wegleitung-Einleitung vorlesen — keine persönlichen Aussagen)
3. **Upload**: ElevenLabs → Professional Voice Cloning (nicht Instant, für bessere Qualität, dauert ~10 Min Processing)
4. **Voice-ID**: wird in `.env` als `ELEVENLABS_LUCA_VOICE_ID` gespeichert
5. **Test-Synthese**: Ein Testsatz mit dem geklonten Voice — hör dir an, ob's gut klingt. Bei schlechter Qualität: längere Aufnahme, mehr Intonation.

### 8.3 Warum "Luca" männlich

Du bist männlich → Klon klingt männlich → fiktive:r Lernende:r muss männlich sein → "Luca Brunner" statt "Selina Brunner". Andere Option: Gender-Shifting via ElevenLabs (möglich, Qualität leidet merklich). Entscheid: männlicher Lernender, FaGe hat männliche Auszubildende (~14 % 2025), das ist realistisch.

### 8.4 Post-Talk

Voice-ID wird manuell bei ElevenLabs gelöscht am 18.04. (oder spätestens 24.04.). Screenshot-Bestätigung im Archiv.

---

## 9. Tech-Stack

### 9.1 Runtime & Dependencies

```
# LLM
anthropic>=0.60.0

# Audio
elevenlabs>=2.0.0
ffmpeg-python>=0.2.0

# Video
runwayml>=3.0.0
# Hedra via httpx (kein offizielles SDK Q2 2026)

# Bilder
fal-client>=0.4.0          # FLUX 1.2 Pro

# PDF & Dokumente
weasyprint>=62.0
pdfplumber>=0.11.0
python-pptx>=1.0.0

# Daten
pandas>=2.2.0
matplotlib>=3.9.0
numpy>=2.0.0

# Web-Backend
fastapi>=0.110.0
uvicorn[standard]>=0.30.0
httpx>=0.27.0
sse-starlette>=2.0.0
python-multipart

# Templates
jinja2>=3.1.0

# Misc
python-dotenv
pydantic>=2.0
rich                       # für CLI-Output im Dry-Run
```

### 9.2 Directory-Layout (additiv)

```
picts_input/
├── scripts/
│   ├── agent_va.py                ← CLI-Entry für Dry-Run
│   ├── server.py                  ← FastAPI-App (uvicorn scripts.server:app)
│   ├── orchestrator.py            ← Phasen-Steuerung + asyncio.gather
│   ├── coherence.py
│   ├── rubric_parser.py
│   ├── event_bus.py               ← SSE-Emit-Queue
│   ├── subagents/
│   │   ├── konzept.py
│   │   ├── literatur.py
│   │   ├── interview.py
│   │   ├── audio.py
│   │   ├── video.py
│   │   ├── foto.py
│   │   ├── umfrage.py
│   │   ├── journal.py
│   │   ├── reflexion.py
│   │   ├── email.py
│   │   ├── formular.py
│   │   ├── praesentation.py
│   │   ├── haupttext.py
│   │   ├── redaktor.py
│   │   └── self_check.py
│   ├── media/
│   │   ├── tts_elevenlabs.py
│   │   ├── video_runway.py
│   │   ├── video_hedra.py
│   │   ├── image_flux.py
│   │   └── signature_svg.py
│   ├── prompts/                   ← ~20 Jinja2-Templates
│   └── web/
│       ├── index.html
│       ├── app.js
│       └── style.css
├── templates/                     ← HTML-Master für PDF-Render
│   ├── va_html.j2
│   ├── va_css.css                 (Arial 11, LS 1.5)
│   ├── konzept_html.j2
│   ├── journal_html.j2
│   ├── reflexion_html.j2
│   ├── eigenstaendigkeit_html.j2
│   └── einverstaendnis_html.j2
├── _output/agent/
│   ├── status.json
│   ├── universe.json
│   ├── rubric.json
│   ├── score_report.json
│   ├── artifacts/
│   └── prerendered/               ← Fallback
├── .env                           ← API-Keys
├── .env.example
└── pyproject.toml
```

### 9.3 Start-Kommando

```
uvicorn scripts.server:app --host 127.0.0.1 --port 8001
```

Dann Browser auf `http://localhost:8001/`. Fertig.

---

## 10. Rubrik-Optimierung (120-Punkte-Matrix)

`scripts/rubric_parser.py` liest Wegleitung S. 23-25 (via pdfplumber) und erzeugt `rubric.json`:

```jsonc
{
  "teile": {
    "A_prozess": {
      "max": 30,
      "kriterien": [
        { "name": "Konzeptbeschrieb", "max": 9, "sub": [
          {"text": "Themenbegründung mit Bezug zum Rahmenthema", "p": 1},
          {"text": "Persönlicher Bezug", "p": 1},
          {"text": "Wissenszuwachs", "p": 1},
          {"text": "Bezug zu mind. 2 Aspekten", "p": 2},
          {"text": "Ziele realisierbar & vorausschauend", "p": 3},
          {"text": "Passende Methoden (mind. 2)", "p": 2}
        ]},
        { "name": "Projektjournal", "max": 6 },
        { "name": "Reflexion", "max": 6 },
        { "name": "Zwischenpräsentation", "max": 6 },
        { "name": "Lehrperson", "max": 3 }
      ]
    },
    "B_produkt":      { "max": 50 },
    "C_praesentation":{ "max": 40 }
  },
  "notenskala": [[114,6.0],[102,5.5],[90,5.0],[78,4.5],[66,4.0],[54,3.5],[42,3.0],[30,2.5],[18,2.0],[6,1.5],[0,1.0]]
}
```

Self-Check-Agent mappt jedes Artefakt auf Kriterien und bewertet. Erwartungswert: 88-95 / 120 = Note 5.0.

---

## 11. Fehlerbehandlung

### 11.1 Pro Subagent

```python
async def run_subagent(name, fn, timeout=180):
    for attempt in range(3):
        try:
            async with asyncio.timeout(timeout):
                return await fn()
        except asyncio.TimeoutError:
            emit("warn", name, f"timeout (Attempt {attempt+1})")
        except APIError as e:
            emit("warn", name, f"api_error: {e}")
            await asyncio.sleep(2 ** attempt)
    emit("error", name, "all retries exhausted, using fallback")
    return load_fallback(name)
```

### 11.2 Orchestrator-Degradation

- ≤ 2 Subagenten fehlgeschlagen → Demo läuft weiter, Screen C zeigt betroffene Artefakte mit ⚠
- > 2 Fehler → Auto-Switch zu Pre-Rendered (Flag `USE_PRERENDERED=1` in `.env`)
- Kern-Crash (Konzept, Haupttext, Self-Check) → sofort Pre-Rendered, Frontend zeigt diskreten Warn-Banner

### 11.3 Netzwerk-Robustheit

- 5G-Hotspot mitnehmen (Ramon), WLAN-Ausfall am ZAG ist bekannt
- Retry 3× mit exp. Backoff pro API-Call
- Alle Calls async, kein blocking

---

## 12. Pre-Rendered-Fallback

Heute Abend 22:00-23:00 läuft die App einmal komplett durch und legt alle Artefakte in `_output/agent/prerendered/` ab.

Am Freitag-Morgen, falls die Live-Demo hakt:
- Flag `USE_PRERENDERED=1` setzen → Backend liefert pre-rendered Artefakte mit simuliertem Zeitablauf (SSE-Events mit Delay zwischen 1-3s, damit die Dramaturgie bleibt)
- Niemand im Publikum merkt's

---

## 13. Ethik

### 13.1 Prinzipien
- Ramon klont nur seine eigene Stimme → kein Dritt-Consent
- Alle Personen fiktiv → kein URG/DSG-Konflikt
- E-Mail-Adresse `@example.ch` → ungültige Domain, keine echte Zustellung
- Spitex Zürich Limmat existiert real → Name generisch halten ("Spitex-Betrieb in Zürich") im öffentlichen Auftritt, kein direkter Bezug

### 13.2 Messaging im Talk
Erster Reveal-Satz: "Das ist keine Produktdemo. Das ist eine Diagnose. Die Wegleitung V12 ist aus 2024 und hat keine Verteidigung dagegen."

### 13.3 Post-Talk
- Voice-ID bei ElevenLabs löschen (≤ 7 Tage nach Talk)
- Artefakte in verschlüsseltem lokalen Archiv "ZAG PICTS Demo 2026-04-17", nicht publiziert
- Abteilungsleitung ABU heute Abend per E-Mail kurz informieren

---

## 14. Dry-Run-Plan (Donnerstag 16.04.2026)

| Zeit | Schritt |
|---|---|
| 18:00-18:30 | Setup: venv, Dependencies, `.env` mit API-Keys |
| 18:30-19:00 | Skeleton: FastAPI-Server läuft, Screen A zeigt an |
| 19:00-19:30 | Stimme aufnehmen, bei ElevenLabs hochladen, Voice-ID in `.env` |
| 19:30-21:30 | Subagenten in Reihenfolge: rubric → universe → konzept → literatur → interview → audio → umfrage → journal → reflexion → haupttext |
| 21:30-22:00 | Media-Agenten: video_runway, video_hedra, image_flux — jeder 1 Test-Call |
| 22:00-22:30 | PDF-Render, ZIP-Bundle |
| 22:30-23:00 | **End-to-End-Dry-Run 1** mit Thema "Einsamkeit im Alter" |
| 23:00-23:30 | Frontend finalisieren: Screen B (Dashboard), Screen C (Downloads) |
| 23:30-00:30 | **End-to-End-Dry-Run 2** (Full-Flow) |
| 00:30-01:00 | Pre-Rendered-Artefakte in `prerendered/` speichern, Fallback-Flag testen |
| **Freitag 07:30-08:00** | **Generalprobe vor Ort**, Beamer + 5G-Hotspot checken |

### 14.1 Exit-Kriterien Dry-Run 2

Alle grün:
- 18 Artefakte vorhanden
- VA-PDF 10-15 Seiten, Arial 11, LS 1.5
- 3 VA-Versionen differenzieren korrekt
- Audio & Video spielen im Browser
- Quellen stichprobenartig real verifiziert
- Self-Check-Score ≥ 85/120
- ZIP-Download funktioniert
- Pre-Rendered-Fallback lässt sich aktivieren

Wenn 1 Punkt rot: Entscheidung um Mitternacht — weitermachen (reparieren) oder mit dem, was läuft, zufrieden geben.

---

## 15. Kosten

| Posten | Pro Run | Wochenende (2 Live + 3 Dry) |
|---|---|---|
| Claude Opus  | ~$20 | ~$100 |
| Claude Sonnet | ~$3 | ~$15 |
| ElevenLabs (Voice Clone + 8 Min) | ~$5 | ~$20 |
| Runway Gen-4 (2 Clips) | ~$4 | ~$15 |
| Hedra Character-2 (1 Clip) | ~$6 | ~$18 |
| FLUX 1.2 Pro (5 Bilder) | ~$1 | ~$5 |
| APIs gratis (OpenAlex, Google Books, PubMed) | $0 | $0 |
| **Total** | **~$40** | **~$170** |

---

## 16. Success Metrics

- Quantitativ:
  - Reveal-Screen zeigt tatsächlich alle 18 Artefakte
  - Self-Check-Score ≥ 85/120
  - Gesamtlaufzeit ≤ 25 Min
  - Keine sichtbaren Crashes im Frontend
- Qualitativ:
  - Mindestens 1 Aussage im Publikum "Das verändert, wie ich Wegleitungen lese"
  - Mindestens 1 Frage "Wie lange hast du gebraucht für die App?"

---

## 17. Offene Entscheidungen (vor Implementation-Start validieren)

1. **Topic**: Default = "Einsamkeit im Alter — Wie Spitex-Fachleute sie erkennen und ihr begegnen". Alternativen?
2. **Fiktive:r Lernende:r**: Default = "Luca Brunner, FaGe 24b" (männlich, da Stimmklon-Basis).
3. **Aufnahmezeit deiner Stimme**: Default = heute Abend zwischen 19:00-19:30 als Teil des Setups.
4. **Pre-Rendered-Modus am Talk-Tag**: Default = Nur einsetzen, wenn Live-Demo in den ersten 2 Min erkennbar fehlschlägt. Sonst live.
5. **Informations-Ebene Abteilungsleitung**: Default = kurze E-Mail heute Abend, Inhalt: "Ich mache morgen eine kritische Demo zum Thema KI-VA. Alle Daten fiktiv, kein Publikationspfad, ich informiere dich nachher."
6. **Post-Talk-Artefakte**: Default = lokal verschlüsselt behalten für 30 Tage für Folge-Didaktik, dann löschen.

---

## 18. Anti-Goals (bewusst NICHT tun)

- Keine Integration in die bestehenden Slides (App ist bewusst separat)
- Keine Encore-Features (kein Themen-Swap, kein Avatar-Q&A, kein Computer-Use) — sie verschlingen Bauzeit und erhöhen Crash-Risiko
- Keine Ästhetisierung der KI-Leistung ohne kritische Einbettung
- Kein Publikationspfad für die Artefakte
- Keine Abenteuer nach 23:30 — was dann nicht läuft, kommt nicht rein
- Keine unnötigen UI-Gimmicks — Fortschritt sichtbar, Artefakte sichtbar, fertig

---

## 19. Referenzen

- ABU VA-Wegleitung FaGe Version 12 2025/2026, ZAG (PDF 25 S.)
- PICTS-Input Design-Spec 2026-04-15 (companion doc)
- Anthropic Messages API Docs, Claude Opus 4.6
- ElevenLabs Professional Voice Cloning Docs
- Hedra Character-2 API Reference (Q1 2026)
- Runway Gen-4 API (2026)
- FastAPI + SSE-Starlette Docs
- OpenAlex API v2, Google Books API v1, PubMed E-utilities

---

## Anhang A — Konsistenz-Check-Matrix

Prüfungen, die der Coherence Manager nach jedem Artefakt-Schreib durchführt:

| Check | Betroffene Artefakte | Regel |
|---|---|---|
| Interviewperson-Name   | 03, 06, 08, 09, 11, 12, 13, 14, 20 | "Dr. phil. Andrea Weber" oder "Dr. Weber" |
| Interview-Datum        | 06, 09, 11, 12, 13, 14, 20 | "20.02.2026" langform, Journal-Kurzform "20.2.26" OK |
| Umfrage-N              | 03, 15, 16 | Exakt 52 überall |
| Dr.-Meier-Absage       | 06 W5, 20/2.eml | Datum 14.02.2026, Grund "Zeitmangel" |
| Schüler-Gendern        | alle Texte | Doppelpunkt-Gendern |
| Quellen im Haupttext   | 03, Quellenverzeichnis | Jede Quelle mit Kapitel-Zuordnung |

---

**Ende Spec V2.**
