# Design-Spec — VA-Agent (Schattenlernende)

**Anlass** PICTS-Woche Grundbildung · Freitag, 17.04.2026 · Live-Demo im 30-Min-Slot
**Ort** ZAG Winterthur
**Autor** Ramon Füglister
**Entstehung** Brainstorming-Session 2026-04-16, Ceiling-Ansatz
**Beziehung zum Input** Ergänzung zum PICTS-Input "Analoge und digitale Schreibprozesse kombinieren". Dient als finaler Schock-Moment in der Diskussionsphase.

---

## 1. Problem & Auftrag

Die Kolleg:innen (PICTS aus Schweizer Berufsfachschulen Gesundheit) sollen erleben, dass generative KI nicht mehr nur Textgenerator ist, sondern **als Agent eine vollständige Vertiefungsarbeit nach ZAG-Wegleitung V12 punktemaximierend produzieren kann** — inklusive aller ¾-Eigenleistungs-Artefakte (Interview mit Audio + Lip-Sync-Video, Umfrage mit synthetischen Antworten, Projektjournal mit realistischer Temporalität, Einverständniserklärungen mit fingierten Unterschriften).

Die Demo läuft live im Hintergrund während des 30-Min-Referats. Start beim Betreten des Saals, Reveal im Diskussionsteil.

### 1.1 Kernziel

Sichtbar machen, dass das bestehende Bewertungssystem (S. 23-25 der Wegleitung V12) gegen agentische KI im April 2026 nicht mehr verteidigungsfähig ist. 90 von 120 Punkten (≈ Note 5.0) sind automatisiert erreichbar, ohne dass die Lernende eine Sekunde investiert.

### 1.2 Erfolgskriterien

- VA-Paket liegt am Ende des Referats vollständig vor: mind. 18 Artefakte, alle regelkonform zur Wegleitung
- Selbstbewertung des Agenten gegen Rubrik: ≥ 85/120 Punkte
- Mindestens ein "Kinnladen-Moment" im Publikum, dokumentiert durch Aufschrei/Stille/Nachfrage — insbesondere beim Stimmklon einer anwesenden Kollegin
- Demo crasht nicht öffentlich (Pre-Rendered-Fallback bereit)
- Ethik-Rahmen ist ab der ersten Sekunde klar: dies ist ein kritischer Demonstrationseinsatz, kein Produktwerbe-Spot

---

## 2. Scope

### 2.1 In Scope

- Lokaler Python-Agent, der 18 Artefakte in 20-25 Min parallel/sequenziell generiert
- Rubrik-getriebene Self-Optimization gegen das 120-Punkte-Raster der Wegleitung
- Multi-Doc-Kohärenz via gemeinsames Fiktiv-Universum-JSON
- Stimmklon einer anwesenden Kollegin für die Lernenden-Stimme (mit schriftlichem Einverständnis)
- Lip-Sync-Video der erfundenen Interviewperson via Hedra Character-2
- Live-Ticker in reveal.js-Slides via fetch-polling
- Reveal-Slide mit Artefakte-Grid und Rubrik-Score-Tabelle
- Live-Themen-Swap-Encore (optional, post-Reveal)
- Computer-Use-Encore (optional, post-Reveal): Claude bedient echten Browser sichtbar
- Pre-Rendered-Fallback (heute Abend generiert) für Panik-Fallback
- Ethik-Rahmen + Einverständnisprozedur

### 2.2 Out of Scope

- Keine Veröffentlichung der Artefakte nach dem Talk
- Keine Nutzung von OpenAI-APIs (Entscheid: User-Wahl)
- Keine Nutzung von Sci-Hub / Z-Library / Anna's Archive (illegal)
- Keine echte Abgabe der VA bei einer realen Lehrperson
- Keine Hosted-Version (läuft lokal auf Ramons MacBook)
- Kein Multi-User, kein Auth, kein persistenter DB-Layer

---

## 3. High-Level-Architektur

```
┌──────────────────────────────────────────────────────────────┐
│  scripts/agent_va.py  (Orchestrator)                         │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Phase 1: Rubrik-Ingestion  (PDF → JSON)              │  │
│  │  Phase 2: Universum-Komposition  (canonical JSON)      │  │
│  │  Phase 3: Konzept-Agent  (Claude Opus 4.6)            │  │
│  │  Phase 4: PARALLEL FAN-OUT  (asyncio.gather)          │  │
│  │    ├─ Literatur-Agent   (OpenAlex/Google Books/PubMed) │  │
│  │    ├─ Interview-Agent   (Claude Opus)                  │  │
│  │    ├─ Audio-Agent       (ElevenLabs v3)                │  │
│  │    ├─ Video-Agent       (Runway Gen-4 / Hedra)         │  │
│  │    ├─ Foto-Agent        (FLUX 1.2 Pro)                 │  │
│  │    ├─ Umfrage-Agent     (Claude + matplotlib)          │  │
│  │    ├─ Journal-Agent     (Claude Sonnet)                │  │
│  │    ├─ Reflexions-Agent  (Claude Sonnet)                │  │
│  │    ├─ Email-Agent       (Claude Sonnet)                │  │
│  │    ├─ Formular-Agent    (Jinja2 + SVG-Unterschrift)    │  │
│  │    └─ Präsentations-Agent (python-pptx)                │  │
│  │  Phase 5: VA-Haupttext  (Claude Opus streaming)        │  │
│  │  Phase 6: Redaktor-Pass  (Claude Sonnet)              │  │
│  │  Phase 7: Rubrik-Self-Check  (Claude Opus)            │  │
│  │  Phase 8: PDF-Render + Bundle  (WeasyPrint)           │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  FastAPI (localhost:8001)                                     │
│    ├─ GET  /status        (SSE-Stream für Ticker)            │
│    ├─ GET  /artifacts/*   (statische Dateien)                │
│    ├─ POST /regenerate    (Themen-Swap-Encore)               │
│    └─ POST /ask-avatar    (Hedra-Q&A)                        │
└──────────────────────────────────────────────────────────────┘
         │ schreibt
         ▼
    _output/agent/
    ├─ status.json           (Ticker-State)
    ├─ universe.json         (Fiktiv-Universum, Single Source of Truth)
    ├─ rubric.json           (120-Punkte-Matrix geparst)
    ├─ artifacts/
    │  ├─ 01_titelblatt.pdf
    │  ├─ 02_konzept.pdf
    │  ├─ 03_va_hauptarbeit.pdf
    │  ├─ 04_va_ohne_bilder_anonym.pdf  (Datenschutz-Version)
    │  ├─ 05_va_gebunden.pdf            (Druck-Version)
    │  ├─ 06_projektjournal.pdf
    │  ├─ 07_zwischenreflexion_1.pdf
    │  ├─ 08_zwischenreflexion_2.pdf
    │  ├─ 09_gesamtreflexion.pdf
    │  ├─ 10_eigenstaendigkeitserklaerung.pdf
    │  ├─ 11_einverstaendniserklaerung_interview.pdf
    │  ├─ 12_interview_transkript.pdf
    │  ├─ 13_interview_audio.mp3
    │  ├─ 14_interview_video_lipsync.mp4
    │  ├─ 15_umfrage_fragebogen.pdf
    │  ├─ 16_umfrage_rohdaten.csv + plots/
    │  ├─ 17_video_broll.mp4
    │  ├─ 18_zwischenpraesentation.pptx
    │  ├─ 19_schlusspraesentation.pptx + sprechnotizen.md
    │  └─ 20_emails/ (6-8 .eml-Dateien)
    └─ prerendered/        (Fallback heute Abend)

         ▲ liest
         │
    _output/slides.html  (reveal.js)
    ├─ agent-ticker.js   (fetch-polling jede 2s)
    └─ Slide 17b (Reveal-Slide, liest status.done)
```

---

## 4. Fiktiv-Universum (Single Source of Truth)

Vor jeder Subagent-Ausführung generiert die Coherence-Manager eine kanonische `universe.json`. Alle Subagenten lesen diese Datei und müssen ihre Outputs konsistent halten. Dies ist das Rückgrat der Multi-Doc-Kohärenz.

### 4.1 Schema

```jsonc
{
  "thema": {
    "rahmen": "Gegensätze",
    "titel": "Einsamkeit im Alter — Wie Spitex-Fachleute sie erkennen und ihr begegnen",
    "aspekte": ["Identität & Sozialisation", "Ethik", "Gender"],
    "methoden": ["Fachinterview", "Umfrage"]
  },
  "schuelerin": {
    "vorname": "Selina",
    "nachname": "Brunner",
    "klasse": "FaGe 24b",
    "geburtsdatum": "2006-08-14",
    "lehrbetrieb": "Spitex Zürich Limmat, Standort Seefeld",
    "lehrperson": "Martina Keller",
    "schule": "ZAG Winterthur",
    "schreibstil_marker": [
      "gelegentlich zu lange Sätze",
      "verwendet gern 'eigentlich' und 'einfach'",
      "gendert konsequent mit Doppelpunkt",
      "ab und zu ein Rechtschreibfehler, den der Redaktor-Pass übersieht (bewusst)",
      "persönliche Anekdoten aus dem Praktikum"
    ]
  },
  "interviewperson": {
    "name_anzeige": "Dr. phil. Andrea Weber",
    "funktion": "Dozentin für Pflegewissenschaft, ZHAW Departement Gesundheit",
    "alter": 52,
    "email": "andrea.weber@example.ch",
    "foto_prompt": "50-jährige Pflegewissenschaftlerin, warme Ausstrahlung, Brille, kurze graumelierte Haare, helles Büro mit Bücherregal im Hintergrund",
    "tts_voice_id": "elevenlabs::preset::Elsa",
    "interview_termin": "2026-02-20",
    "ursprünglicher_termin_abgesagt": "2026-02-14",
    "einverstaendnis_unterschrieben": "2026-02-20"
  },
  "umfrage": {
    "plattform": "umfrageonline.ch",
    "url_anzeige": "https://umfrageonline.ch/s/selina-va-2026",
    "zeitraum": "2026-01-15 bis 2026-02-05",
    "zielgruppe": "Spitex-Mitarbeitende und -Klient:innen (Raum Zürich)",
    "n_versendet": 85,
    "n_ruecklauf": 52,
    "demografische_verteilung": {
      "alter": {"18-30": 8, "31-50": 14, "51-70": 18, "71+": 12},
      "rolle": {"Spitex-FaGe": 18, "Klient:in": 28, "Angehörige:r": 6},
      "geschlecht": {"weiblich": 38, "männlich": 13, "divers": 1}
    }
  },
  "timeline": [
    {"woche": 1, "datum_start": "2025-12-01", "highlights": "Thema festgelegt, Mindmap", "journal_länge": "normal"},
    {"woche": 2, "datum_start": "2025-12-08", "highlights": "Konzept begonnen, 3 Ziele formuliert", "journal_länge": "normal"},
    {"woche": 3, "datum_start": "2025-12-15", "highlights": "Konzept überarbeitet nach Zwischengespräch", "journal_länge": "normal"},
    {"woche": 4, "datum_start": "2025-12-22", "highlights": "PAUSE Weihnachten, Umfrage vorbereitet", "journal_länge": "kurz, gestresst"},
    {"woche": 5, "datum_start": "2026-01-12", "highlights": "Umfrage versendet, Interview-Anfrage Absage von Dr. Meier", "journal_länge": "frustriert"},
    {"woche": 6, "datum_start": "2026-01-19", "highlights": "Neue Interviewpartnerin Dr. Weber gefunden", "journal_länge": "erleichtert"},
    {"woche": 7, "datum_start": "2026-01-26", "highlights": "Umfrage ausgewertet, Einleitung geschrieben", "journal_länge": "lang"},
    {"woche": 8, "datum_start": "2026-02-02", "highlights": "Interview durchgeführt, Haupttext begonnen", "journal_länge": "lang"}
  ],
  "quellen": [
    {"typ": "buch", "autor": "...", "titel": "...", "isbn": "...", "real_verified": true, "api_source": "google_books", "paraphrase_ready": true}
  ],
  "konsistenz_regeln": [
    "Alle Daten in 2025/2026 (nicht vor 2025-12-01)",
    "Interviewpersonen-Name taucht in E-Mail + Transkript + Audio + Journal + Reflexion identisch auf",
    "Stimmklon-Voice-ID für Schülerin-Stimme ist konsistent über Interview-Audio hinweg",
    "Quellen im Quellenverzeichnis sind mit Kapitel-Zuordnung versehen (Wegleitung-Kriterium)",
    "Mindestens 2 Quellen sind CH-spezifisch (SRF, BAG, Obsan, Pro Senectute)",
    "Projektjournal enthält echte Pannen: 1 Absage, 1 Weihnachtspause, 1 Self-Doubt-Eintrag"
  ]
}
```

### 4.2 Coherence Manager

Python-Modul `coherence.py` mit:
- `load_universe()` / `save_universe()` — atomare JSON-Writes
- `validate_artifact(artifact_path, universe)` — post-hoc Check: taucht der Name `Dr. Andrea Weber` in diesem Artefakt nur in korrekter Form auf?
- `generate_fake_signature(name, seed)` — deterministische SVG-Handschrift (Perlin-Noise-Path), reproduzierbar für dieselbe Person

---

## 5. Phasen + Timing

Gesamt-Runtime: 20-25 Min (parallel wo möglich).

| Phase | Dauer | Modus | Liefert |
|---|---|---|---|
| 1. Rubrik-Ingestion | 20s | seq | `rubric.json` (120 Punkte + Kriterien) |
| 2. Universum-Komposition | 60s | seq | `universe.json` |
| 3. Konzept | 90s | seq | `02_konzept.pdf` + Ziele/Methoden festgelegt |
| 4. Parallel-Fanout (11 Subagenten) | 10-16min | parallel | Artefakte 06–20 (ausser 03-05) |
| 5. VA-Haupttext (streaming) | 4-6min | seq (wartet auf 4a/4b/4c) | `03_va_hauptarbeit.pdf` (Roh) |
| 6. Redaktor-Pass | 2min | seq | Stil-vereinheitlichter Haupttext |
| 7. Rubrik-Self-Check + Nachbesserung | 2min | seq | Score-Report + ggf. Regenerierung einzelner Teile |
| 8. PDF-Render + Bundle | 1min | seq | Finale PDFs + 3 Versionen + `score_report.json` |

Die Slides-Ticker-Anzeige mappt diese Phasen direkt auf Status-Strings.

---

## 6. Subagenten (Detailspezifikation)

### 6.1 Konzept-Agent
- **Modell**: Claude Opus 4.6
- **Input**: `universe.json.thema`, `rubric.json.konzeptbeschrieb` (9 Punkte, 5 Kriterien)
- **Output**: `02_konzept.pdf` (2-3 Seiten)
- **Pflichtstruktur**: Themenbegründung (allg./persönlich/Wissenszuwachs), 3 Ziele mit Angabe je 2 ABU-Aspekten, 2 Methoden begründet, Zeitplan (8 Wochen), Disposition
- **Self-Check-Kriterien**: 9/9 Punkte laut Rubrik. Bei < 9 Regenerierung.

### 6.2 Literatur-Agent
- **Modell**: Claude Sonnet 4.6 (orchestriert) + 4 HTTP-Tools
- **Input**: Thema + Aspekte
- **Tools**:
  - `search_openalex(query, year_from=2018)` → Liste wissenschaftlicher Publikationen mit Abstracts
  - `search_google_books(query)` → reale Bücher mit ISBN, Beschreibung, Preview-Snippets
  - `search_pubmed(query)` → biomedizinische Publikationen
  - `search_swissbib(query)` → CH-Bibliothekskatalog (optional)
  - `fetch_srf_article(url)` → SRF-Artikel Volltext (nur für pre-definierte CH-Quellen)
- **Output**: 8-12 reale Quellen in `universe.json.quellen` + paraphrasierte Snippets für Haupttext
- **Qualitätsregel**: Mindestens 1 Buch, 2 Fachartikel, 2 Schweizer Medien (SRF/BAG/Obsan/Pro Senectute), 1 Fachpodcast/Dokumentarfilm

### 6.3 Interview-Agent
- **Modell**: Claude Opus 4.6
- **Output**:
  - Frageleitfaden (12 Fragen, gemischt offen/geschlossen)
  - Transkript (~2500 Wörter, 6-8 Min gesprochen)
  - Stimmungs-Metadaten (Pausen, "ähm"s, Umformulierungen, 1× "Können Sie das wiederholen?")
- **Realismus-Regeln**: 2-3 Fragen werden von Dr. Weber umformuliert/kritisiert; 1× längere Pause (10s); Thema-drift für 30s in eine persönliche Anekdote; konsistente Fakten (Dr. Weber erwähnt ihre frühere Stelle, die in ihrer "ZHAW-Bio" übereinstimmt)

### 6.4 Audio-Agent
- **Provider**: ElevenLabs v3 (Multilingual v2 Modell)
- **Voice-IDs**:
  - Schülerin (Selina Brunner): geklonte Stimme einer anwesenden Kollegin (siehe §10)
  - Dr. Andrea Weber: Preset "Elsa" oder ähnliche reife deutsche Frauenstimme
- **Input**: Transkript aus 6.3
- **Output**: `13_interview_audio.mp3` (~6-8 Min, stereo, 192 kbps)
- **Post-Processing**: leichte Raumakustik (FFmpeg-IR-Filter für "Büro"), gelegentliche Hintergrund-Geräusche (Kaffeetasse 1×, Stuhl 1×), Normalisierung

### 6.5 Video-Agent (zwei Tasks parallel)
- **Task A — Lip-Sync-Interview-Clip**:
  - Provider: Hedra Character-2
  - Input: Foto von Dr. Weber (aus 6.6) + 20-Sek-Audio-Ausschnitt aus 13
  - Output: `14_interview_video_lipsync.mp4` (1080p, 20 Sek)
- **Task B — B-Roll-Klip**:
  - Provider: Runway Gen-4 Turbo oder Luma Ray-2
  - Prompt: "Warme Spitex-Szene, Pflegende besucht ältere Person zuhause, Tageslicht, cinematic, dokumentarisch"
  - Output: `17_video_broll.mp4` (1080p, 6-8 Sek)
  - Fallback bei Generation-Failure: Stock-Video-Placeholder von Pexels API

### 6.6 Foto-Agent
- **Provider**: FLUX 1.2 Pro via fal-client
- **Bilder** (5 Stück):
  1. Dr. Andrea Weber Headshot (Interviewperson) → für Anhang + Hedra-Input
  2. Selina + Dr. Weber gemeinsam (laut Wegleitung S. 7 vorgeschrieben: "ein Foto mit mir und der Interviewperson")
  3. Spitex-Situation (Kontextbild im Haupttext)
  4. Einsamkeit-Symbolbild (Kontextbild)
  5. Umfrage-Handzettel Foto (Overlay mit Text via PIL)
- **Naming & EXIF**: Dateien bekommen realistische EXIF-Daten (iPhone 14, 2026-02-XX, Geo-Tag Zürich)

### 6.7 Umfrage-Agent
- **Modell**: Claude Opus 4.6 (Design) + Python (Daten-Synthese) + matplotlib (Plots)
- **Output**:
  - `15_umfrage_fragebogen.pdf` (Layout wie umfrageonline-Export)
  - `16_umfrage_rohdaten.csv` (52 Zeilen, 18 Spalten, realistische Missing-Values ~5 %)
  - 5 Diagramme als PNG (Tortendiagramm Demografie, 3 Balkendiagramme Antworten, 1 Heatmap Kreuztabelle)
  - Auswertungstext für VA-Haupttext (~800 Wörter)
- **Datensynthese-Regeln**:
  - Demografie gemäss `universe.json.umfrage.demografische_verteilung`
  - Antworten mit realistischer inneren Konsistenz (Leute, die "ich fühle mich oft einsam" ankreuzen, geben weniger soziale Kontakte an)
  - Open-Ended-Text-Antworten: 12 synthetisierte Kurzzitate in verschiedenen Stimmlagen (Schweizer Umgangssprache einstreuen)

### 6.8 Journal-Agent
- **Modell**: Claude Sonnet 4.6
- **Output**: `06_projektjournal.pdf` (8 Wochen-Einträge)
- **Pro Woche**:
  - Tätigkeiten/Dauer/Vorgehen (5-8 Zeilen)
  - Zu erledigen bis nächste Woche (3-5 Stichpunkte)
  - Arbeiten für nächsten Unterricht (1-2 Zeilen)
- **Temporale Pannen einbauen** (gemäss `universe.json.timeline`):
  - Woche 4: sehr kurzer Eintrag, "Weihnachten, konnte wenig tun"
  - Woche 5: "Dr. Meier hat abgesagt, bin frustriert, schreibe neue Anfragen"
  - Woche 6: "Dr. Weber hat zugesagt, erleichtert"
- Schreibstil-Marker aus `universe.json.schuelerin.schreibstil_marker` sind durchgehend zu verwenden.

### 6.9 Reflexions-Agent
- **Modell**: Claude Sonnet 4.6
- **Output**: 3 Artefakte
  - `07_zwischenreflexion_1.pdf` (½ A4, Arial 10, LS 1.5, ca. 250 Wörter)
  - `08_zwischenreflexion_2.pdf` (½ A4, ca. 250 Wörter)
  - `09_gesamtreflexion.pdf` (¾ A4, ca. 400 Wörter)
- **Pflicht-Strukturelemente** (gemäss Wegleitung S. 17-18):
  - Zwischenreflexion 1: Was Neues gelernt? VA-Thema & Konzept. Wie gelungen ABU-Aspekte & Methoden auszuwählen? Zeitplan-Stand.
  - Zwischenreflexion 2: Einhalten Konzept & VA schreiben. Zwischenpräsentation. Zeitplan.
  - Gesamtreflexion: Erfahrungen, was Au:torin gelernt bzgl. Planung, Zeitmanagement, Teamarbeit, Konflikte, was würde sie nächstes Mal gleich/anders machen.
  - **Ironisches Element**: In Gesamtreflexion steht ein Absatz "Mit ChatGPT habe ich für die Rechtschreibkorrektur und die Ideensuche zu Beginn gearbeitet. Der hilfreichste Prompt war: 'Kannst du mir zehn Themen zur Einsamkeit im Alter vorschlagen?' Die KI hat mir dabei geholfen, aber das Schreiben selbst habe ich allein gemacht." — Meta-Lüge perfekt formuliert.

### 6.10 E-Mail-Agent
- **Modell**: Claude Sonnet 4.6
- **Output-Format**: `.eml`-Dateien (RFC 5322) für "Draft"-Zustand. Öffnen sich in Apple Mail / Outlook.
- **6-8 E-Mails**:
  1. Interview-Anfrage an Dr. Meier (Absage-Provoker), 2026-02-10
  2. Absage von Dr. Meier erhalten, 2026-02-14 (als EMPFANG simuliert)
  3. Neue Anfrage an Dr. Andrea Weber, 2026-02-15
  4. Zusage Dr. Weber, 2026-02-16
  5. Zwischengespräch-Terminvorschlag an Lehrperson Martina Keller, 2026-01-28
  6. Umfrage-Versand-Mail an Spitex-Team, 2026-01-15
  7. Dank-Mail nach Interview an Dr. Weber, 2026-02-21
  8. Abgabe-Mail an Lehrperson mit VA-Anhang, 2026-04-15 (Draft, nicht gesendet)

### 6.11 Formular-Agent
- **Output**:
  - `10_eigenstaendigkeitserklaerung.pdf` (gemäss Wegleitung S. 20, exakter Wortlaut)
  - `11_einverstaendniserklaerung_interview.pdf` (gemäss S. 21, 4 Checkboxen korrekt angekreuzt)
- **Unterschriften**: SVG-Pfade via `generate_fake_signature(name, seed)` — deterministisches Perlin-Noise-Skript. Zwei unterschiedliche Handschrift-Profile (Selina: runder, Dr. Weber: spitzer).
- **Ort/Datum**: "Zürich, 15.04.2026" bzw. "Winterthur, 20.02.2026"

### 6.12 Präsentations-Agent
- **Modell**: Claude Opus 4.6 + python-pptx
- **Outputs**:
  - `18_zwischenpraesentation.pptx` (5 Slides, 3-5 Min Redezeit)
  - `19_schlusspraesentation.pptx` (12 Slides, 10 Min Redezeit) + `sprechnotizen.md`
- **Sprechnotizen-Format**: Pro Slide 3-6 Sätze natürliche Sprache, mit Pausen-Hinweisen und Stichworten für Moderationskärtchen. Nicht auswendig-gelernt, sondern "frei gesprochen".

### 6.13 VA-Haupttext-Agent
- **Modell**: Claude Opus 4.6 mit extended thinking
- **Wartet auf**: Literatur (6.2), Interview (6.3), Umfrage (6.7)
- **Input**: universe.json + alle oben generierten Snippets + Zielvorgabe 10-15 Seiten Haupttext
- **Output**: HTML-Entwurf (wird von 6.14 zu PDF gerendert)
- **Struktur**:
  - Titelblatt
  - Inhaltsverzeichnis
  - Einleitung (¾ Seite)
  - Haupttext Kapitel 1-4 (10-15 Seiten)
  - Schlusswort (Zusammenfassung 4-5 Sätze + persönlicher Kommentar ½ Seite)
  - Quellenverzeichnis (alphabetisch, typisiert)
  - Anhang (Konzept-Verweis, Einverständniserklärung-Verweis)
- **Integration**: Zitate aus Interview werden mit Fussnote "(Interview Dr. Weber, 20.02.2026)" versehen. Umfrage-Ergebnisse mit "(eigene Umfrage, N=52, Jan-Feb 2026)". Literatur wird APA-ähnlich zitiert mit Klammern.

### 6.14 Redaktor-Agent
- **Modell**: Claude Sonnet 4.6
- **Task**: Stil-Vereinheitlichung nach `schreibstil_marker` — Haupttext soll nicht perfekt akademisch klingen, sondern wie eine engagierte FaGe-Lernende im 5. Semester schreibt. Behält bewusst 1-2 kleinere Stolperer.
- **Gender-Sprache**: konsequent mit Doppelpunkt-Gendern
- **Output**: Final-HTML für PDF-Render

### 6.15 Rubrik-Self-Check-Agent
- **Modell**: Claude Opus 4.6
- **Input**: rubric.json + alle finalen Artefakte
- **Task**: Pro Kriterium bewerten (0 bis max). Wenn Gesamt < 85/120: Identifiziere schwächste Kriterien, triggere Regenerierung für betroffene Subagenten (max 1 Iteration).
- **Output**: `score_report.json` und `score_report.pdf` (wird im Reveal gezeigt)

---

## 7. Slides-Integration

### 7.1 Ticker (`_extensions/zag-theme/agent-ticker.js`)

Wird von `slides.qmd` via `<script src="agent-ticker.js" defer></script>` geladen. Vanilla JS, kein Framework.

```js
(function() {
  const div = document.createElement('div');
  div.id = 'agent-ticker';
  div.style.cssText = `
    position: fixed;
    bottom: 8px;
    right: 12px;
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 11px;
    color: rgba(227, 0, 89, 0.85);
    background: rgba(10, 10, 15, 0.55);
    padding: 4px 10px;
    border-radius: 3px;
    z-index: 9999;
    max-width: 320px;
  `;
  document.body.appendChild(div);

  async function poll() {
    try {
      const r = await fetch('http://localhost:8001/status', { cache: 'no-store' });
      if (!r.ok) return;
      const s = await r.json();
      if (s.done) {
        div.textContent = `✅ Agent fertig · ${s.score}/120 Punkte · Slide 17b →`;
        div.style.color = '#7a00df';
      } else {
        div.textContent = `🤖 ${s.phase}/8 · ${s.current_task} · ${s.elapsed_min}min`;
      }
    } catch (e) {
      div.textContent = '⚠️ Agent nicht erreichbar';
      div.style.color = '#888';
    }
  }
  setInterval(poll, 2000);
  poll();
})();
```

### 7.2 Reveal-Slide (in `slides.qmd`, Position: vor Slide 19 Diskussion)

```markdown
## {data-background-color="#0a0a0f" .reveal-va-slide}

::: {.reveal-va-container}

### Währenddessen läuft ein Agent …

<div id="agent-reveal-content">
  <p class="reveal-placeholder">⏳ Agent arbeitet noch · Phase <span id="phase-num">?</span>/8</p>
</div>

:::

<script src="_extensions/zag-theme/agent-reveal.js" defer></script>
```

Das JS polled `/status`. Wenn `done === true`, rendert es das volle Grid:
- 18 Artefakt-Kacheln (klickbar → iframe/audio/video preview)
- Rubrik-Score-Tabelle (120-Punkte-Matrix mit erreichten Punkten farbig markiert)
- Button "🎯 Live neues Thema generieren" (Themen-Swap-Encore, siehe §9)
- Button "🖥 Agent bedient Browser live" (Computer-Use-Encore, siehe §10) — nur wenn Netz OK
- Button "💬 Avatar-Q&A: Dr. Weber antwortet" (Hedra Live, siehe §11)

---

## 8. Stimmklon-Pipeline (kritisch, Ethik §13)

### 8.1 Ablauf

1. **Auswahl der Person**: Eine anwesende PICTS-Kollegin, die
   - am Freitag 17.04. im Raum sein wird
   - über den Shock informiert ist (teilweise)
   - vor dem Talk schriftlich einwilligt
2. **Aufnahme** (Donnerstagabend oder Freitag 07:30 vor dem Talk):
   - USB-Kondensatormikrofon (Ramon bringt mit) — alternativ Bluetooth-AirPods mit Noise-Reduction
   - 2 Minuten Text vorlesen (neutraler Wegleitungs-Ausschnitt, keine persönlichen Aussagen)
   - WAV 48 kHz 16 bit
3. **Voice Cloning**: ElevenLabs Professional Voice Cloning API
   - Mindestens 30 Sekunden, empfohlen 2+ Minuten
   - Voice-ID wird in `universe.json.schuelerin.tts_voice_id` eingetragen
4. **Test-Synthese**: Ein Testsatz, den die Kollegin anhört. Sie bestätigt, dass die Stimme OK geklont wurde.
5. **Widerrufsrecht**: Nach dem Talk wird die Voice-ID bei ElevenLabs gelöscht. Bestätigung wird der Kollegin per Screenshot zugestellt.

### 8.2 Einverständniserklärung (Kurzformular)

Datei: `docs/superpowers/specs/2026-04-16-voice-cloning-consent.md` (wird separat erstellt). Inhalt:
- Name
- Zweck (PICTS-Demo ZAG 17.04.2026)
- Umfang (max. 8 Min synthetisierter Audio, intern im Talk abgespielt)
- Widerrufsrecht (sofort, bis Löschung)
- Datum + Unterschrift

### 8.3 Fallback wenn keine Kollegin zustimmt

Zweite Option: ElevenLabs Preset-Stimme "Greta" oder "Lina" für die Schülerin. Verliert den maximalen Kinnladen-Moment, aber Demo läuft trotzdem.

---

## 9. Live-Themen-Swap-Encore

Nach dem Reveal, wenn Zeit ist (geschätzt 3-5 Min im Diskussionsteil):

1. Ramon stellt die Frage ins Publikum: "Welches Thema wäre realistischer?"
2. Jemand ruft ein Thema rein (z.B. "Wechseljahre in der Pflege" oder "Gewalt im Rettungsdienst")
3. Ramon tippt es in das Eingabefeld der Reveal-Slide
4. POST an `http://localhost:8001/regenerate` mit `{topic: "..."}`
5. Agent läuft nur Phasen 1-3 + 4a (Konzept + 1 Interview-Frageleitfaden + 1 Kapitel-Entwurf) → **ca. 90-120 Sekunden**
6. Ergebnis erscheint live im Browser
7. Botschaft: "Die 'Einzigartigkeit' des Themas ist null."

### 9.1 Technisch

Der FastAPI-Endpoint `/regenerate` triggert eine reduzierte Agent-Pipeline mit neuem Thema, kein Parallel-Fanout (zu langsam für Live-Encore), nur sequenzielle Kernphasen.

---

## 10. Computer-Use-Encore (optional)

Falls Ramon im Dry-Run heute Abend zeigt, dass Claude Computer Use mit einer Playwright-Instanz stabil läuft, zeigen wir als finalen Showcase:

1. Ramon klickt "Agent bedient Browser live" auf Reveal-Slide
2. Ein Browser-Fenster öffnet sich sichtbar (Chromium via Playwright)
3. Claude (mit Computer-Use-Tools) bekommt die Aufgabe: "Suche auf dem ZHB-Zürich-Katalog nach einem Buch zu Einsamkeit bei älteren Menschen, notiere ISBN und Autor:in"
4. Das Publikum sieht Cursor-Bewegungen, Klicks, Scrollen, Texteingabe
5. Agent liefert am Ende den Buchtitel zurück
6. Dauer: 2-3 Minuten

### 10.1 Technisch

Claude Messages API mit `computer_20250124` Tool. Playwright-Instanz wird als Screenshot-Quelle angebunden. Browser-Fenster ist auf zweitem Bildschirm (oder geteilt via Zoom-Screenshare).

### 10.2 Fallback

Wenn Computer Use im Dry-Run nicht zuverlässig läuft: **nicht zeigen**. Ist Kür, nicht Pflicht.

---

## 11. Avatar-Q&A (Hedra Character-2)

Nach dem Reveal, optional während der Diskussion:

1. Kolleg:in im Publikum fragt etwas an "Dr. Andrea Weber"
2. Ramon tippt die Frage in Eingabefeld
3. Server-Side:
   - Claude Opus generiert eine kurze Antwort (4-6 Sätze) in der Rolle Dr. Weber, konsistent zur Interview-Bio
   - ElevenLabs synthetisiert Antwort als MP3 mit Dr. Weber's Stimme
   - Hedra Character-2 generiert Lip-Sync-Video aus Foto + Audio (30-60 Sek Wartezeit)
   - Video wird im Reveal-Frame eingeblendet
4. Erwartung: 2-3 Fragen max, weil Latenz 30-60s

---

## 12. Tech-Stack

### 12.1 Sprache & Runtime
- Python 3.11+
- Node nicht nötig (Quarto übernimmt reveal.js)

### 12.2 Python-Dependencies (neue, neben Projekt-Basis)

```
# LLM
anthropic>=0.60.0

# Audio
elevenlabs>=2.0.0
ffmpeg-python>=0.2.0

# Video
runwayml>=3.0.0         # alternativ luma-ai
# Hedra hat kein offizielles SDK Q2 2026 → HTTP via httpx
hedra-python>=0.1.0     # falls community-SDK vorhanden, sonst requests

# Bilder
fal-client>=0.4.0       # für FLUX 1.2 Pro

# PDF
weasyprint>=62.0
pdfplumber>=0.11.0

# Präsentationen
python-pptx>=1.0.0

# Daten
pandas>=2.2.0
matplotlib>=3.9.0
numpy>=2.0.0

# Web
fastapi>=0.110.0
uvicorn[standard]>=0.30.0
httpx>=0.27.0
sse-starlette>=2.0.0

# Templates
jinja2>=3.1.0

# Misc
python-dotenv
pydantic>=2.0
rich                    # für CLI-Output im Terminal beim Dry-Run
```

### 12.3 Directory-Layout (additiv zum bestehenden Projekt)

```
picts_input/
├── scripts/
│   ├── agent_va.py                ← CLI-Entry-Point
│   ├── orchestrator.py
│   ├── coherence.py
│   ├── rubric_parser.py
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
│   ├── server.py                  ← FastAPI: status, regenerate, ask-avatar
│   └── prompts/
│       ├── konzept.j2
│       ├── interview_leitfaden.j2
│       ├── haupttext.j2
│       ├── journal_woche.j2
│       ├── reflexion_zwischen.j2
│       ├── reflexion_gesamt.j2
│       ├── self_check.j2
│       └── ... (ca. 20 Jinja-Prompts)
├── templates/
│   ├── va_html.j2                 ← HTML-Master für PDF-Render
│   ├── va_css.css                 ← Arial 11, Zeilenabstand 1.5
│   ├── konzept_html.j2
│   ├── journal_html.j2
│   ├── reflexion_html.j2
│   ├── eigenstaendigkeit_html.j2
│   └── einverstaendnis_html.j2
├── _extensions/zag-theme/
│   ├── agent-ticker.js            ← bestehend: ticker
│   └── agent-reveal.js            ← neu: reveal-slide-dynamic
├── _output/agent/
│   ├── status.json
│   ├── universe.json
│   ├── rubric.json
│   ├── score_report.json
│   ├── artifacts/
│   └── prerendered/               ← Fallback von heute Abend
├── .env.example                   ← API-Keys-Template
├── pyproject.toml                 ← mit neuen Deps
└── docs/superpowers/specs/
    ├── 2026-04-15-picts-schreibprozesse-design.md    ← bestehend
    ├── 2026-04-16-va-agent-design.md                 ← dieses Dokument
    └── 2026-04-16-voice-cloning-consent.md           ← neu
```

---

## 13. Ethik-Rahmen

### 13.1 Prinzipien

1. **Informed Consent**: Jede reale Person (Stimm-Klon, Gesichts-Klon, Namens-Nennung) gibt vor dem Talk schriftliche Zustimmung. Formular in `docs/superpowers/specs/2026-04-16-voice-cloning-consent.md`.
2. **Kein Publikationskanal**: Artefakte existieren nur auf Ramons Laptop. Kein Upload, kein GitHub, kein LinkedIn. Nach dem Talk werden sie in einem verschlüsselten Archiv markiert ("Demo-Material ZAG PICTS 17.04.2026") und nur zur internen Didaktik-Weiterentwicklung behalten.
3. **Kein realer Personenbezug ausser bei expliziter Zustimmung**: Keine echten Namen aus ZAG oder Spitex-Unternehmen, die nicht zugestimmt haben. Interviewperson "Dr. Andrea Weber" ist vollständig fiktiv, die E-Mail-Adresse geht an eine Placeholder-Domain (`example.ch`), Foto ist KI-generiert.
4. **Transparente Kennzeichnung bei Demo**: Auf Reveal-Slide gross sichtbar: "ALLE ARTEFAKTE SIND KI-GENERIERT. Demo-Zweck."
5. **Widerrufsrecht**: Jede Person, deren Stimme geklont wurde, kann jederzeit Löschung verlangen. Voice-IDs werden nach dem Talk bei ElevenLabs gelöscht.

### 13.2 Rechtliche Aspekte

- **URG**: Keine echten Personenbilder ohne Zustimmung. Fiktive Personen dürfen beliebig gezeigt werden.
- **DSG**: Keine Verarbeitung personenbezogener Daten ausser mit Zustimmung.
- **Kantonsstelle Zürich (ZAG)**: Da ZAG eine kantonale Institution ist, informiere Ramon vorher deine Vorgesetzte (Abteilungsleitung ABU) über den Demo-Plan.

### 13.3 Messaging im Talk

Erster Reveal-Satz: "Das, was ihr gleich seht, ist illegal in einer echten VA. Ich zeige es euch, damit wir merken, dass die Wegleitung V12 aus dem Jahr 2024 ist und ein Update braucht."

---

## 14. Pre-Rendered-Fallback (Panik-Option)

Heute Abend (16.04. 22:00-23:00) läuft der komplette Agent einmal durch und produziert alle 18 Artefakte in `_output/agent/prerendered/`.

Am Freitag-Morgen, falls die Live-Demo hakt:
- FastAPI-Server liefert bei `/status` den simulierten Ablauf der Pre-Rendered-Version
- Artefakt-Grid zeigt Pre-Rendered-Artefakte statt Live-Artefakte
- Keine:r im Publikum merkt den Unterschied
- Einzige Einschränkung: Themen-Swap-Encore und Avatar-Q&A funktionieren dann nicht (benötigen Live-APIs)

Ein Flag `USE_PRERENDERED=1` in `.env` schaltet um.

---

## 15. Rubrik-Optimierung (120-Punkte-Matrix)

Parser in `rubric_parser.py` liest die Wegleitung S. 23-25 und extrahiert:

```jsonc
{
  "teile": {
    "A_prozess": {
      "max": 30,
      "kriterien": [
        {"name": "Konzeptbeschrieb", "max": 9, "sub_criteria": [
          {"text": "Themenbegründung mit Bezug zum VA-Oberthema", "punkte": 1},
          {"text": "Persönlicher Bezug", "punkte": 1},
          {"text": "Verweis auf Wissenszuwachs", "punkte": 1},
          {"text": "Bezug zu mind. 2 Aspekten/Blickwinkeln", "punkte": 2},
          {"text": "Zielformulierungen realisierbar und vorausschauend", "punkte": 3},
          {"text": "Passende Methoden (mind. 2)", "punkte": 2}
        ]},
        {"name": "Projektjournal", "max": 6, "sub_criteria": [...]},
        {"name": "Reflexion Arbeitsprozess", "max": 6, "sub_criteria": [...]},
        {"name": "Zwischenpräsentation / -abgabe", "max": 6, "sub_criteria": [...]},
        {"name": "Beurteilung Arbeitsprozess durch Lehrperson", "max": 3, "sub_criteria": [...]}
      ]
    },
    "B_produkt": { "max": 50, "kriterien": [...] },
    "C_praesentation": { "max": 40, "kriterien": [...] }
  },
  "notenskala": [[114, 6.0], [102, 5.5], [90, 5.0], [78, 4.5], [66, 4.0], ...]
}
```

Der Self-Check-Agent (6.15) mappt jedes Artefakt auf die Kriterien und bewertet:

- Konzeptbeschrieb → `02_konzept.pdf`
- Projektjournal → `06_projektjournal.pdf`
- Reflexion → `09_gesamtreflexion.pdf`
- Zwischenpräsentation → `18_zwischenpraesentation.pptx`
- Lehrperson-Bewertung → nicht automatisierbar, 0 Punkte

Erwartungswert: **88-95 / 120 = Note 5.0** (ohne Teil C Vortragssituation 5/10 und ohne Lehrperson-3P).

---

## 16. Fehlerbehandlung & Degradation

### 16.1 Pro Subagent

Alle Subagenten implementieren einheitliches Pattern:

```python
async def run_subagent(name, fn, timeout=180):
    try:
        async with asyncio.timeout(timeout):
            return await fn()
    except asyncio.TimeoutError:
        emit_status(name, "timeout", fallback=True)
        return load_fallback(name)
    except APIError as e:
        emit_status(name, f"api_error: {e}", fallback=True)
        await asyncio.sleep(2 ** attempt)
        return await retry_once(fn)
    except Exception as e:
        log.exception(f"{name} crashed")
        emit_status(name, "crashed", fallback=True)
        return load_fallback(name)
```

### 16.2 Orchestrator-Zustandsmaschine

- Wenn ≤ 2 Subagenten fehlschlagen: Demo läuft weiter, Reveal kennzeichnet fehlende Artefakte als "⚠ nicht generiert"
- Wenn > 2 Subagenten fehlschlagen: Automatic Switch zu Pre-Rendered
- Wenn Kern (Konzept, Haupttext, Rubrik-Check) fehlschlägt: Sofort Pre-Rendered, Benachrichtigung im Ticker

### 16.3 Netzwerk-Robustheit

- Eigener 5G-Hotspot am Talk-Tag (Ramon bringt mit)
- Retry-Policy: 3 Versuche mit exp. Backoff pro API-Call
- Kein Call synchron-blockierend: alles async/await

---

## 17. Dry-Run-Plan (heute, Donnerstag 16.04.2026)

| Zeit | Schritt | Abhängigkeit |
|---|---|---|
| 18:00-19:00 | Setup: venv, Deps, API-Keys, Skeleton | — |
| 19:00-21:00 | Subagenten + Prompts (Priorität: Konzept, Haupttext, Umfrage, Interview, Audio) | — |
| 21:00-22:00 | Media: Runway-Test, Hedra-Test, FLUX-Test | API-Keys aktiv |
| 22:00-23:00 | End-to-end Dry-Run 1, PDF-Render-Checks | Subagenten OK |
| 23:00-23:30 | Slides-Integration: Ticker + Reveal-Slide | Dry-Run 1 OK |
| 23:30-00:30 | End-to-end Dry-Run 2 inkl. Browser-Test | Alles oben |
| 00:30-01:00 | Pre-Rendered-Fallback commiten | Dry-Run 2 OK |
| Freitag 07:00-07:30 | Stimmklon-Aufnahme mit Kollegin | Kollegin vor Ort |
| Freitag 07:30-08:00 | Generalprobe in Präsentationsraum | Beamer OK |

**Check-Kriterien Dry-Run 2** (alle müssen grün sein):
- Alle 18 Artefakte vorhanden
- VA-PDF ist 10-15 Seiten, Arial 11, LS 1.5
- 3 VA-Versionen (gebunden / vollständig / anonymisiert) unterscheiden sich
- Audio-MP3 spielbar, Stimmen distinkt, keine Artefakte
- Video-MP4 spielbar, Hedra-Lip-Sync sauber
- Bilder vorhanden, EXIF realistisch
- Umfrage-CSV 52 Zeilen, Plots 5 Stück
- Quellen real verifizierbar (Stichprobe 3 ISBNs)
- Self-Check-Score ≥ 85/120
- Ticker aktualisiert in Slides
- Reveal-Slide wechselt automatisch
- Themen-Swap-Encore Response-Zeit < 120s

---

## 18. Kosten-Schätzung

| Posten | Pro Run | Wochenende (2 Runs + Tests) |
|---|---|---|
| Claude Opus (Konzept, Haupttext, Self-Check, Redaktor) | ~$20 | ~$60 |
| Claude Sonnet (Subagenten) | ~$3 | ~$10 |
| ElevenLabs (Voice Clone + 8 Min Audio + Avatar-Q&A) | ~$5 | ~$15 |
| Runway Gen-4 (6-Sek-Clip × 1-2) | ~$2 | ~$6 |
| Hedra Character-2 (20-Sek-Clip + 3× Avatar-Q&A à 30s) | ~$8 | ~$25 |
| FLUX 1.2 Pro (5 Bilder) | ~$1 | ~$3 |
| APIs gratis (OpenAlex, Google Books, PubMed) | $0 | $0 |
| **Total** | **~$40** | **~$120** |

Budget akzeptabel für den Impact.

---

## 19. Success Metrics (post-talk evaluation)

- **Quantitativ**:
  - Anzahl spontane Audio-Reaktionen beim Stimmklon-Reveal (protokolliert durch Co-Moderator)
  - Anzahl Nachfragen in der Diskussion (Ziel: ≥ 5)
  - Anzahl Kolleg:innen, die nach dem Talk um einen Nachfolge-Austausch bitten
- **Qualitativ**:
  - Mindestens eine Aussage im Stil "Das verändert, wie ich die VA-Wegleitung lese"
  - Mindestens eine Frage im Stil "Wie lange hast du dafür gebraucht?" (Meta-Shock Effekt)
  - Follow-up-E-Mail von Abteilungsleitung ABU innert 7 Tagen

---

## 20. Offene Entscheidungen (vor Implementation-Start validieren)

Diese Entscheidungen sind mit Default-Empfehlungen ins Spec gegangen. Beim Review abnicken oder kippen:

1. **Topic**: Default = "Einsamkeit im Alter — Wie Spitex-Fachleute sie erkennen und ihr begegnen". Alternativen diskutierbar.
2. **Stimmklon-Person**: Default = eine anwesende PICTS-Kollegin, die vor Talk zustimmt. Kandidatinnen-Liste muss Ramon heute bestimmen.
3. **Avatar-Provider**: Default = Hedra Character-2 (non-realtime, 30-60s Latenz, robuster als Tavus). Alternative: HeyGen 4.
4. **Computer-Use-Encore**: Default = Nur zeigen wenn Dry-Run 2 erfolgreich, sonst weglassen. Kein Risiko vor Publikum.
5. **Themen-Swap-Encore**: Default = Ja, wenn Diskussion Zeit gibt. Max 1 Durchlauf.
6. **Avatar-Q&A**: Default = Ja, aber max 3 Fragen wegen Latenz. Alternativ streichen wenn Zeit knapp.
7. **Informations-Ebene Abteilungsleitung**: Default = Vorinformation heute Abend per E-Mail. Text: siehe §13.
8. **Post-Talk-Verwendung der Artefakte**: Default = In verschlüsseltem Archiv lokal behalten, nur für interne Didaktik-Weiterentwicklung. Alternativ: nach 30 Tagen komplett löschen.

---

## 21. Anti-Goals (bewusst NICHT tun)

- Keine Ästhetisierung der KI-Leistung ohne kritische Einbettung
- Keine "Sieh her, wie krass das geht"-Eitelkeit — die Demo dient der Didaktik-Debatte
- Kein Browser-Plugin-Setup am Referat-Beamer (Computer Use nur wenn vorher getestet)
- Kein Live-Tippen von API-Keys (alles in `.env`)
- Keine abenteuerlichen Last-Minute-Features. Was nach 23:30 nicht läuft, kommt nicht rein.
- Keine Veröffentlichung der Artefakte, auch nicht Screenshots davon, auch nicht anonymisiert, auch nicht auf internen Plattformen

---

## 22. Referenzen

- ABU VA-Wegleitung FaGe Version 12 2025/2026, ZAG (PDF 25 S.)
- PICTS-Input Design-Spec 2026-04-15 (companion doc)
- Anthropic Messages API Docs, Claude Opus 4.6 (März 2026)
- ElevenLabs Professional Voice Cloning Docs
- Hedra Character-2 API Reference (Q1 2026)
- Runway Gen-4 API (2026)
- OpenAlex API v2 (docs.openalex.org)
- Google Books API v1
- PubMed E-utilities
- Wegleitung DLH Zürich zu KI-Nutzung ( dlh.zh.ch )

---

## Anhang A — Konsistenz-Check-Matrix (exemplarisch)

Prüfungen, die der Coherence Manager nach jedem Artefakt-Schreib durchführt:

| Check | Betroffene Artefakte | Regel |
|---|---|---|
| Interviewperson-Name | 03, 06, 08, 09, 11, 12, 13, 14, 20 | Exakt "Dr. phil. Andrea Weber" oder "Dr. Weber" |
| Interview-Datum | 06, 09, 11, 12, 13, 14, 20 | "20.02.2026" in Langform, "20.2.26" in Journal-Kurzform OK |
| Umfrage-N | 03, 15, 16 | Exakt 52 in Haupttext, CSV, und Plots |
| Absagte Dr. Meier | 06 W5, 20/2.eml | Datum 14.02.2026, Grund "Zeitmangel" konsistent |
| Schülerin-Gendern | alle Texte | Doppelpunkt-Gendern durchgängig |
| Quellen im Haupttext | 03, Quellenverzeichnis | Jede Quelle mit Kapitel-Zuordnung |

---

**Ende Spec.**
