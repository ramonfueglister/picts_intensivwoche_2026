# PICTS-Input · Analoge und digitale Schreibprozesse kombinieren

**Wie KI und analoge Methoden den Schreibprozess gemeinsam bereichern**

PICTS-Woche Grundbildung · Freitag, 17.04.2026 · ZAG Winterthur
Ramon Füglister · ABU · 30 Minuten

---

## 🎯 Schnellzugriff

| Artefakt | Pfad | Zweck |
|---|---|---|
| 📊 **Präsentation (HTML)** | [`_output/slides.html`](_output/slides.html) | Im Browser am Beamer zeigen |
| 📋 **Cheat-Sheet A4 (PDF)** | [`_output/handout/cheatsheet.pdf`](_output/handout/cheatsheet.pdf) | Ausdrucken für alle Teilnehmenden |
| 📄 **Schülertext Hands-on (PDF)** | [`_output/handout/schuelertext-mira-imhof.pdf`](_output/handout/schuelertext-mira-imhof.pdf) | Ausdrucken für alle Teilnehmenden |
| ✍️ **Prompt-Sammlung** | [`handout/prompt-sammlung.md`](handout/prompt-sammlung.md) | 12 getestete Prompts für ABU |
| 📚 **Literatur (60 Quellen)** | [`docs/literature/2025-2026-KI-Schreibunterricht.md`](docs/literature/2025-2026-KI-Schreibunterricht.md) | Alle APA 7, alle 2025/26 |
| 🌍 **Praxis-Beispiele weltweit (30 Fälle)** | [`docs/praxis-beispiele/2025-2026-KI-Schreiben-weltweit.md`](docs/praxis-beispiele/2025-2026-KI-Schreiben-weltweit.md) | CH · DE · AT · USA · UK · AUS · Asien · LatAm · NL · SE |
| 📋 **Design-Spec** | [`docs/superpowers/specs/2026-04-15-picts-schreibprozesse-design.md`](docs/superpowers/specs/2026-04-15-picts-schreibprozesse-design.md) | Warum genau so aufgebaut |

---

## 🏗 Aufbau der Präsentation (14 Slides · 30 Min.)

Dramaturgie: **Problem → Frage → Vier Phasen → Montag → Abschluss**

| Min. | Slide | Inhalt |
|---|---|---|
| 00:00–00:40 | 1 | Titel |
| 00:40–01:20 | 2 | Kunstwerk-Animation (Tri-System, Cognitive Surrender) |
| 01:20–04:20 | 3 | Was Sie eben gesehen haben — und warum das Sorgen macht (Doshi&Hauser + Shaw&Nave + Sanz-Tejeda PRISMA) |
| 04:20–05:20 | 4 | Drei Fragen für die nächsten 25 Minuten (Handzeichen-Erhebung) |
| 05:20–07:20 | 5 | Vier Phasen, ein Prinzip (Hayes&Flower + Analog-first) |
| 07:20–11:20 | 6 | Phase 1 Planen (Blume/Mollick/Kentz + Schneegaß + Levine) |
| 11:20–15:20 | 7 | Phase 2 Strukturieren (UNC/Oxford/iArgue + Philipp) |
| 15:20–19:20 | 8 | Phase 3 Formulieren (Wampfler/LSE/Roberts + Freinhofer PCRR) |
| 19:20–23:20 | 9 | Phase 4 Überarbeiten (Haverkamp/Mollick/Kentz + Rezat + Alnemrat) |
| 23:20–25:20 | 10 | Drei Entscheidungen vor Montag (Prüfung · Datenschutz · Klassenregel) |
| 25:20–28:20 | 11 | Anwendungsphase · Fallarbeit |
| 28:20–29:20 | 12 | Drei Antworten auf drei Fragen (Rückkehr zu Slide 4) |
| 29:20–29:50 | 13 | Materialien · Tools · Repo |
| 29:50–30:00 | 14 | Literatur · Diskussion |

---

## 🎨 Design

- **Farben:** ZAG Magenta `#e30059`, ZAG Lila `#7a00df` (aus `zag.zh.ch` verifiziert)
- **Schrift:** IBM Plex Sans (Open Source)
- **Technik:** Quarto + revealjs, `embed-resources: true` (offline lauffähig)
- **Mockup-Strategie:** echte Screenshots öffentlicher Blogs / Tools / Open-Access-Artikel + CSS-Cards für Layout

---

## 🔬 Zielpublikum-Fokus (ZAG Healthcare-ABU)

Alle Beispiele sind auf Schweizer Gesundheitsberufe (FaGe, FaBe, AGS, HF Pflege) zugeschnitten:

- **Hands-on:** FaGe-Bewerbungstext "Mira Imhof" (realistischer Erstentwurf mit typischen Schwächen)
- **Einstieg CH1:** Careum Verlag · **Navira** KI-Lerncoach im FaBe-Lehrmittel (SJ 2025/26)
- **Einstieg CH2:** **DLH Sek II Kanton ZH** · BS Bülach — VA-Prozess mit KI
- **Einstieg CH3:** **Philippe Wampfler** · UZH/PHZH — Schreibarbeiten mit KI
- **Einstieg US:** **John Warner** — *More than Words* (die kritische Stimme)
- **Reflexions-Prompt:** Pflegepraktikum ("Rolle im Team · Gefühle · Lernzuwachs")
- **Differenzierung:** Sprachniveau-Anpassung (B1/B2) für heterogene FaGe-Klassen
- **Übertragbarkeit:** Pflegedokumentation, Praktikumsbericht, Reflexion nach Einsatz, Fachbericht

---

## 📂 Repo-Struktur

```
picts_input/
├── README.md                            ← du bist hier
├── _quarto.yml                          Quarto-Konfiguration
├── slides.qmd                           Hauptpräsentation (21 Slides)
├── _extensions/zag-theme/zag.scss       SCSS-Theme mit ZAG-Farben
├── _output/                             ← generierte HTML/PDFs
│   ├── slides.html                      Präsentation (offline-lauffähig)
│   └── handout/
│       ├── cheatsheet.pdf               A4 1-Seiten-Cheat-Sheet
│       └── schuelertext-mira-imhof.pdf  Hands-on-Material
├── images/
│   ├── einstieg/                        8 Website-Screenshots
│   ├── literature-figures/              5 Figuren aus Open-Access-Papers
│   ├── literature-pdfs/                 7 Original-PDFs (Referenz)
│   └── phase1-planen/, phase2-…, …/     Phasen-spezifische Bilder
├── handout/
│   ├── cheatsheet.qmd + cheatsheet.css
│   ├── schuelertext-mira-imhof.qmd + schuelertext.css
│   └── prompt-sammlung.md               12 getestete Prompts
└── docs/
    ├── literature/
    │   └── 2025-2026-KI-Schreibunterricht.md   60 Quellen APA 7
    └── superpowers/
        └── specs/
            └── 2026-04-15-picts-schreibprozesse-design.md
```

---

## 🖥 Präsentation rendern (lokal)

```bash
# Quarto installiert (empfohlen: ≥ 1.6)
quarto render slides.qmd --to revealjs

# Handouts
cd handout
quarto render cheatsheet.qmd
quarto render schuelertext-mira-imhof.qmd

# PDF-Export via Chrome headless (falls LaTeX/TinyTeX nicht installiert)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=cheatsheet.pdf \
  "file://$(pwd)/../_output/handout/cheatsheet.html"
```

---

## 📅 Am Präsentationstag (Checkliste)

**Vorabend 16.04.:**
- [ ] `slides.html` rendern, offline testen am eigenen Laptop
- [ ] Cheat-Sheet PDF drucken (N_Teilnehmende + 5 Reserve)
- [ ] Schülertext PDF drucken (gleiche Anzahl)
- [ ] QR-Code testen (muss Repo erreichen)
- [ ] Reserve-Laptop klären (falls Gruppe ohne Gerät)

**Am Ort vor 08:00:**
- [ ] Beamer-Kabel (HDMI / Mini-DP / USB-C)
- [ ] Auflösung 1280×720 oder 1920×1080
- [ ] Browser Vollbild, revealjs-Navigation (← → Esc)
- [ ] WLAN-Zugangsdaten für Hands-on am Flipchart
- [ ] Cheat-Sheets und Schülertexte auf Tischen

---

## 🔁 Wiederverwendung

Die Struktur ist als **Vorlage** für weitere Schreib-Inputs an anderen Berufsschulen konzipiert. Zum Anpassen:

1. **Zielgruppe**: Schülertext, Einstieg-Kacheln und Reflexions-Prompts austauschen
2. **Farben**: `_extensions/zag-theme/zag.scss` — `$primary`, `$secondary` anpassen
3. **Literatur**: `docs/literature/…md` → die 8 inline zitierten Quellen auf dein Fach anpassen

---

## 📖 Verwendete Literatur (Kernauswahl, alle 2025/26)

1. Sanz-Tejeda et al. (2026), *Frontiers in Education* — Review 136 Studien
2. Kızıltaş (2025), *JECR* — empirisch: KI-Feedback & Selbstwirksamkeit
3. Hwang et al. (2025), *JSLW* — wann nutzen Lernende KI?
4. Mei et al. (2025), *Computers in Human Behavior: AH* — Kreativität vs. Output-Qualität
5. Levine et al. (2025), *JAAL* — qualitative Studie Sek-Lernende
6. Steinhoff & Lehnen (2025), *Leseräume 12(11)* — Ghost/Partner/Tutor
7. Tour & Zadorozhnyy (2025), *JAAL* — Prompt Literacy als Lernziel
8. Zhang et al. (2025), *IiLLT* — hybrides Feedback > allein
9. Warner (2025) — *More than Words* (Basic Books)
10. ICT-Berufsbildung Schweiz (2025) — Berufsbildung CH

**Vollständige Liste mit 60 Quellen:** [`docs/literature/2025-2026-KI-Schreibunterricht.md`](docs/literature/2025-2026-KI-Schreibunterricht.md)

---

## 📜 Lizenz & Nutzung

- Content (Text, Konzept, Schülertext): CC BY-SA 4.0 — weiterverbreitung mit Namensnennung erlaubt
- Screenshots fremder Seiten: Bildungszitat nach CH-URG Art. 19 + 25 — Quellen auf den Slides jeweils unten angegeben
- Literatur-Figuren: aus Open-Access-Artikeln (CC BY) — Quellen auf den Slides vermerkt

---

## ✉️ Kontakt

**Ramon Füglister** · Berufsfachschullehrperson ABU
ZAG · Zentrum für Ausbildung im Gesundheitswesen Kanton Zürich · Turbinenstrasse 5, Winterthur
ramon.fuglister@zag.zh.ch
