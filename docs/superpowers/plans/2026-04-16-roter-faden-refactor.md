# Roter Faden · Radikales Refactoring der Präsentation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development oder superpowers:executing-plans zur Umsetzung. Die Schritte nutzen Checkbox-Syntax.

**Goal:** Die Präsentation von 24 auf 15–16 Slides straffen und in eine klare Drei-Akte-Dramaturgie (Problem → Praxis → Montag) umbauen, sodass jede Folie einen zwingenden Platz im Narrativ hat und die Eingangs-Leitfragen am Ende explizit beantwortet werden.

**Architecture:** Vier systemische Probleme lösen: (1) Ausgangslage kommt zu spät, (2) Empirische Befundlage ist redundant mit Slides 2+3, (3) Weltreise dupliziert Phasen-Namen, (4) Phasen brauchen 8 Slides für 4 Konzepte. Lösung: Merging-Slides, Rückbezug-Logik, Reduktion auf narratives Gerüst.

**Tech Stack:** Quarto + revealjs, bestehende zag-theme.scss (keine Änderungen), reiner slides.qmd-Umbau.

---

## Ultrakritische Diagnose je Slide (aktueller Stand, 24 Slides)

| # | Slide | Funktion | Kritik |
|---|---|---|---|
| 1 | Artwork-Animation | Wow-Opener | ✓ funktioniert |
| 2 | "Die Kunst..." Doshi&Hauser | Kreativität +/− | ⚠ linker Textblock zu textig; 3 Evidenz-Kästen für einen Punkt |
| 3 | "Drei Systeme, drei Risiken" Shaw&Nave | Problem | ⚠ Slides 2+3 behandeln beide die KI-Ambivalenz — doppelter Impact verpufft |
| 4 | Ausgangslage 3 Leitfragen | Erhebung | ⚠ kommt nach zwei inhaltsstarken Befund-Slides — wirkt administrativ statt spannungsaufbauend |
| 5 | Empirische Befundlage 5+1 | Evidenz | ⚠ redundant — Doshi&Hauser auf 2, Shaw&Nave auf 3 — verbleiben Sanz-Tejeda, Kızıltaş, Alnemrat, Mei, Weidlich. Zu viele für einen Slot |
| 6 | 4-Phasen-Rahmen | Theorie | ⚠ Hayes&Flower-Credit fehlt; Ursprungs-Quelle wirkt unklar |
| 7 | Analog-first-Prinzip | Faustregel | ⚠ steht isoliert zwischen Theorie und Praxis — könnte direkt in Slide 6 integriert werden |
| 8 | Weltreise 8 Tiles | Fallauswahl | ✗ **dupliziert** — Mollick/Kentz/Haverkamp/Roberts tauchen in Phasen-Slides erneut auf |
| 9–16 | Phasen 1–4 (je 2 Slides) | Praxis | ⚠ 8 Slides für 4 Konzepte — könnten gemergt werden |
| 17 | Prüfung & Datenschutz | Pragmatik | ✗ **Position falsch** — kommt nach 8 Phasen-Slides, wirkt nachgeschoben. Müsste VOR den Phasen stehen als "was Sie wissen müssen, bevor Sie los machen" |
| 18 | Anwendungsphase Fallarbeit | Hands-on | ✓ OK mit neuer Datenschutz-Warnung |
| 19 | Synthese 3 Leitsätze | Abschluss | ✗ **greift Ausgangs-Leitfragen nicht auf** — verlorene Dramaturgie-Chance |
| 20 | Weiterführende Materialien | Handout | ⚠ ABU-Lehrbuch-Duktus passt nicht zur Animation-Ästhetik |
| 21 | Claude Desktop | Tool | ⚠ werblich und redundant — Co-Produktions-Meta steht schon auf Slide 2 |
| 22 | Literatur | Referenz | ✓ OK |
| 23 | Diskussion | Ende | ✓ OK |

**Kernbefund:** Die Präsentation hat eine logische Abfolge, aber kein Narrativ. Jede Folie ist für sich interessant, aber der Sog fehlt. Nach Folie 17 könnte man aufhören — das ist das Symptom.

---

## Neu-Architektur: Vier Akte, 16 Slides (inkl. Artwork)

```
AKT I — Problem (3 Min)
  1  Titel
  2  Animation
  3  "Was Sie eben gesehen haben — und warum uns das Sorgen machen sollte"
     [Doshi&Hauser + Shaw&Nave + Sanz-Tejeda PRISMA in EINER Slide]

AKT II — Frage (1 Min)
  4  "Drei Fragen — drei Handzeichen"
     [Ausgangs-Leitfragen explizit als Spanne, die Slide 12 auflöst]

AKT III — Vier Phasen (16 Min)
  5  "Vier Phasen, ein Prinzip"
     [4-Phasen-Rahmen MIT Analog-first-Faustregel MIT Hayes&Flower-Credit]
  6  Phase 1 Planen — Workflow (Blume/Mollick/Kentz) + Schneegaß empirisch
  7  Phase 2 Strukturieren — Workflow (UNC/Oxford/iArgue) + Philipp PHZH
  8  Phase 3 Formulieren — Workflow (Wampfler/LSE/Roberts) + Freinhofer PCRR
  9  Phase 4 Überarbeiten — Workflow (Haverkamp/Mollick/Kentz) + Rezat+Alnemrat

AKT IV — Montag (8 Min)
  10 "Drei Entscheidungen bevor Sie loslegen" — Prüfung · Datenschutz · Klassenregel
  11 Anwendungsphase — Fallarbeit (Hands-on)
  12 "Drei Antworten auf drei Fragen" — Synthese MIT expliziter Rückkehr zu Slide 4

AKT V — Abschluss (2 Min)
  13 Materialien · Claude Desktop · Repo (integrierte Ende-Slide)
  14 Literatur
  15 Diskussion
```

**Reduktion:** 24 → 15 Slides. 9 Slides entfallen oder werden gemergt:
- Empirische-Befundlage-Slide WEG (Evidenzen auf Slide 3 konzentriert)
- Analog-first-Slide MERGED in 4-Phasen-Slide
- Weltreise-Slide WEG (Namen kommen in Phasen zurück)
- 4× Phase-Empirie-Slide MERGED mit Workflow-Slide
- Claude-Desktop-Slide MERGED in Materialien

**Gewinn:** Jede Slide hat jetzt ~120 Sek statt 75 Sek — mehr Atmung, bessere Anchoring.

---

## Datei-Inventar

**Zu modifizieren:**
- `slides.qmd` — substanzieller Refactor (24 → 15 Slides)
- `README.md` — Dramaturgie-Tabelle aktualisieren (15 Slides)

**Unverändert:**
- `_extensions/zag-theme/zag.scss` (keine CSS-Änderungen nötig — alle Klassen bleiben)
- Alle Bilder, Screenshots, Literatur-PDFs (keine neuen Assets)
- `docs/literature/` (bleibt)

---

## Task 1: Slide "Was Sie eben gesehen haben — und warum uns das Sorgen machen sollte"

Mergt die zwei getrennten Slides (Doshi&Hauser / Shaw&Nave) in **eine** spannungsstarke Slide, die Lob UND Warnung in einem Frame auflöst.

**Files:**
- Modify: `slides.qmd` — ersetze die zwei Slides "## Die Kunst, die Sie gerade gesehen haben —" (Zeile 85) und "## Drei Systeme, drei Risiken" (Zeile 124) durch eine einzige gemergte Slide

- [ ] **Step 1: Aktuelle Slides 2 und 3 identifizieren**

```bash
cd /Users/ramonfuglister/Desktop/Coding/picts_input
grep -n "^## Die Kunst\|^## Drei Systeme" slides.qmd
```

Erwartung: zwei Zeilennummern. Alles zwischen Slide 2 und "## Ausgangslage" ersetzen.

- [ ] **Step 2: Beide Blöcke durch neuen Merge-Block ersetzen**

Verwende Edit-Tool mit diesem `old_string` (Beginn):
```
## Die Kunst, die Sie gerade gesehen haben —
```

Bis Beginn der Ausgangslage-Slide (nicht inklusive):
```
## Ausgangslage
```

Ersetze mit:

```markdown
## Was Sie eben gesehen haben — und warum das Sorgen macht

<div style="display: grid; grid-template-columns: 1.1fr 1fr; gap: 1.3rem; margin-top: 0.4em;">

<div>

<p style="font-size: 1.05em; line-height: 1.55; margin-bottom: 0.9em;">
<em>Konzept · Wortauswahl · Timing · Farbcode · CSS — die Animation stammt zu 100 % von Claude.</em>
</p>

<div class="evidence fragment" data-fragment-index="1">
<div class="evidence-label">Empirisch · KI-Kreativität</div>
<div class="evidence-text">KI-Ideen machen Kurzgeschichten <strong>signifikant kreativer, besser geschrieben, unterhaltsamer</strong> — besonders bei weniger geübten Schreibenden (N = 293).</div>
<div class="evidence-source"><a href="https://www.science.org/doi/10.1126/sciadv.adn5290" target="_blank">Doshi &amp; Hauser (2024)</a>, <em>Science Advances 10</em>(28).</div>
</div>

<div class="evidence fragment" data-fragment-index="2" style="border-left-color: #ff1744; margin-top: 0.7em;">
<div class="evidence-label" style="color:#ff1744;">Empirisch · Cognitive Surrender</div>
<div class="evidence-text">Akkuratheit <strong>+25 pp</strong> bei korrekter KI · <strong>−15 pp</strong> bei fehlerhafter (N = 1 372). System 1 wird betäubt, System 2 umgangen, System 3 denkt ausserhalb.</div>
<div class="evidence-source"><a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6097646" target="_blank">Shaw &amp; Nave (2026)</a>, SSRN · Wharton · Tri-System-Theorie.</div>
</div>

<div class="evidence fragment" data-fragment-index="3" style="border-left-color: #7a00df; margin-top: 0.7em;">
<div class="evidence-label" style="color:#7a00df;">Systematisches Review</div>
<div class="evidence-text">136 Studien zu KI im Schreibprozess — wirkt, aber ausschliesslich bei didaktischer Einbettung.</div>
<div class="evidence-source"><a href="https://doi.org/10.3389/feduc.2025.1711718" target="_blank">Sanz-Tejeda et al. (2026)</a>, <em>Frontiers in Education 10</em>, 1711718.</div>
</div>

</div>

<div class="fragment" data-fragment-index="4" style="display: flex; flex-direction: column; gap: 0.8rem; justify-content: center;">

<div style="text-align: center; padding: 1.2rem 1rem; background: #1a1a1a; color: white; border-radius: 10px;">
<div style="font-size: 1.15em; line-height: 1.4; font-weight: 700; letter-spacing: -0.01em;">
Individuell kreativer.<br>
<span style="color: #ff5994;">Kollektiv einförmiger.</span><br>
<span style="color: #ff1744;">Kognitiv kapitulierend.</span>
</div>
</div>

<a class="linked-img" href="https://doi.org/10.3389/feduc.2025.1711718" target="_blank">
<img src="images/literature-figures/sanz-tejeda-prisma-geo.png" style="width: 100%; border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" alt="PRISMA 136 Studien">
</a>
<p class="credit" style="text-align: center;">Sanz-Tejeda et al. (2026) · PRISMA-Flussdiagramm &amp; geografische Verteilung</p>

</div>

</div>
```

- [ ] **Step 3: Rendern**

```bash
export PATH="$HOME/tools/bin:$PATH"
quarto render slides.qmd --to revealjs 2>&1 | tail -3
```

- [ ] **Step 4: Visuelle Verifikation**

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p _check/rf
"$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars --screenshot="_check/rf/s2-merged.png" --window-size=1280,720 --virtual-time-budget=5000 "file://$(pwd)/_output/slides.html#/1" 2>/dev/null
```

Read `_check/rf/s2-merged.png`. Erwartung: Titel "Was Sie eben gesehen haben — und warum das Sorgen macht", links drei Evidenz-Kästen (Doshi&Hauser/Shaw&Nave/Sanz-Tejeda) als Fragments, rechts schwarzer Hero-Block mit dreiteiliger Punchline + PRISMA-Bild.

---

## Task 2: Slide "Drei Fragen — drei Handzeichen" (Ausgangslage neu)

**Files:**
- Modify: `slides.qmd` — Slide "## Ausgangslage" (Zeile 170) überarbeiten

Die Eingangs-Leitfragen werden expliziter als **Spanne formuliert**, die am Ende der Präsentation geschlossen wird. Plus direkter Anknüpfungspunkt an die vorhergehenden Befunde.

- [ ] **Step 1: Slide "Ausgangslage" finden und ersetzen**

Ersetze den gesamten Block von `## Ausgangslage` bis zur nächsten `##`-Überschrift durch:

```markdown
## Drei Fragen für die nächsten 25 Minuten

<div style="font-size: 1.05em; margin-top: 0.6em; line-height: 1.55; color: #4a4a4a;">
Die Studienlage ist klar — aber was heisst das für den Montag-Unterricht am ZAG? Drei Fragen führen durch den Rest dieses Inputs:
</div>

<ol style="margin-top: 1.2em; font-size: 1.05em; line-height: 1.65;">
<li><strong>Welche Forschungsevidenz 2025/26</strong> ist für den Schreibunterricht in Gesundheitsberufen handlungsleitend?</li>
<li><strong>Wie kombinieren</strong> erfahrene Lehrpersonen und Hochschuldozierende analoge und KI-gestützte Arbeit <strong>konkret</strong>?</li>
<li><strong>Welche drei Entscheidungen</strong> müssen Sie vor Montag treffen, damit der Einsatz didaktisch und rechtlich belastbar ist?</li>
</ol>

<div class="evidence" style="margin-top: 1.3em; border-left-color: #7a00df;">
<div class="evidence-label" style="color:#7a00df;">Erhebung im Plenum</div>
<div class="evidence-text">Wer nutzt generative KI bereits in einer Schreibaufgabe mit Lernenden? <strong>Abstufung 0–3 per Handzeichen</strong> — damit ich sehe, auf welchem Stand Sie sind.</div>
</div>

<div style="margin-top: 1em; font-size: 0.8em; color: #888; font-style: italic;">
Auf diese drei Fragen kommen wir auf Slide 12 zurück.
</div>
```

- [ ] **Step 2: Rendern & Screenshot**

```bash
export PATH="$HOME/tools/bin:$PATH"
quarto render slides.qmd --to revealjs 2>&1 | tail -3
"$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars --screenshot="_check/rf/s3-ausgang.png" --window-size=1280,720 --virtual-time-budget=4000 "file://$(pwd)/_output/slides.html#/2" 2>/dev/null
```

Read und verifizieren: drei nummerierte Fragen, Handzeichen-Box, Ausblick-Hinweis.

---

## Task 3: Empirische-Befundlage-Slide entfernen

**Files:**
- Modify: `slides.qmd` — Slide "## Empirische Befundlage 2025/26" (Zeile 187) komplett entfernen

Begründung: Doshi&Hauser, Shaw&Nave, Sanz-Tejeda sind auf Slide 2 integriert. Kızıltaş, Alnemrat, Mei, Weidlich bleiben in der Literaturfolie und im Repo — für den Vortrag nicht zentral.

- [ ] **Step 1: Slide-Block komplett löschen**

Suche und entferne alles zwischen `## Empirische Befundlage 2025/26` und der nächsten `## `-Überschrift.

```bash
grep -n "^## Empirische Befundlage\|^## Theoretischer Rahmen" slides.qmd
```

Erwartung: zwei Zeilennummern. Alles dazwischen (inklusive der Empirische-Befundlage-Zeile, exklusive der Theoretischer-Rahmen-Zeile) wird entfernt.

Verwende Edit-Tool mit dem gesamten Block als `old_string` und einer leeren Zeile als `new_string` (also: entferne komplett).

- [ ] **Step 2: Verifikation**

```bash
grep -c "^## Empirische Befundlage" slides.qmd
```

Erwartung: `0`.

---

## Task 4: 4-Phasen-Rahmen + Analog-first in EINER Slide vereinen

**Files:**
- Modify: `slides.qmd` — zwei Slides "## Theoretischer Rahmen..." und "## Didaktisches Prinzip..." werden zu einer zusammengeführt.

- [ ] **Step 1: Beide Slides durch Merge-Slide ersetzen**

Suche den Bereich von `## Theoretischer Rahmen: Schreibprozess als rekursives Modell` bis zum Beginn von `## Dokumentierte Unterrichtspraxis` und ersetze komplett mit:

```markdown
## Vier Phasen, ein Prinzip

<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.6rem; margin-top: 1em;">
<div style="background: rgba(122,0,223,0.08); padding: 0.9rem; border-radius: 8px; border-left: 3px solid #7a00df;">
<h3 style="color: #7a00df; margin-top: 0; font-size: 1.15em;">1 · Planen</h3>
<div style="font-size: 0.8em;">Ideen finden, Thema klären, Material sammeln</div>
</div>
<div style="background: rgba(122,0,223,0.08); padding: 0.9rem; border-radius: 8px; border-left: 3px solid #7a00df;">
<h3 style="color: #7a00df; margin-top: 0; font-size: 1.15em;">2 · Strukturieren</h3>
<div style="font-size: 0.8em;">Ordnen, Gliederung entwickeln</div>
</div>
<div style="background: rgba(227,0,89,0.08); padding: 0.9rem; border-radius: 8px; border-left: 3px solid #e30059;">
<h3 style="color: #e30059; margin-top: 0; font-size: 1.15em;">3 · Formulieren</h3>
<div style="font-size: 0.8em;">Entwerfen, Sätze bauen</div>
</div>
<div style="background: rgba(227,0,89,0.08); padding: 0.9rem; border-radius: 8px; border-left: 3px solid #e30059;">
<h3 style="color: #e30059; margin-top: 0; font-size: 1.15em;">4 · Überarbeiten</h3>
<div style="font-size: 0.8em;">Prüfen, überdenken, Feinschliff</div>
</div>
</div>

<div style="margin-top: 0.9em; font-size: 0.78em; color: #888; text-align: center;">
Rekursive Rücksprünge zwischen allen Phasen · nach Hayes &amp; Flower (1980) · erweitert bei Kellogg (1996 ff.) · angewandt auf KI-Kontexte bei Schneegaß (2025)
</div>

<div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 1.5rem; margin-top: 1.5em; align-items: center;">

<div style="text-align: center; font-size: 1.4em; color: #e30059; font-weight: 700; line-height: 1.25; padding: 1.2rem; background: rgba(227,0,89,0.06); border-radius: 12px; border-left: 4px solid #e30059;">
Eigenständige Konzeptarbeit<br>→ KI-Input<br>→ begründete Entscheidung
</div>

<div style="font-size: 0.85em; line-height: 1.55; color: #4a4a4a;">
<strong>Analog-first</strong> als Faustregel — gestützt durch zwei Befunde:

<ul style="margin-top: 0.5em;">
<li>Lernende nutzen KI am intensivsten beim <strong>Planen</strong>, kaum beim Überarbeiten — <a href="https://doi.org/10.1016/j.jslw.2025.101230" target="_blank">Hwang et al. (2025)</a></li>
<li>KI hebt Qualität, senkt aber Motivation und Autor:innenschaft — <a href="https://doi.org/10.1016/j.chbah.2025.100140" target="_blank">Mei et al. (2025)</a></li>
</ul>

<div style="margin-top: 0.6em; font-size: 0.8em; color: #888;">
Ausnahmen: Recherche bei fehlendem Vorwissen · standardisierte Textsorten · produktive Blockaden.
</div>
</div>

</div>
```

- [ ] **Step 2: Rendern und visuell prüfen**

```bash
export PATH="$HOME/tools/bin:$PATH"
quarto render slides.qmd --to revealjs 2>&1 | tail -3
"$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars --screenshot="_check/rf/s5-phasen.png" --window-size=1280,720 --virtual-time-budget=4000 "file://$(pwd)/_output/slides.html#/4" 2>/dev/null
```

---

## Task 5: Weltreise-Slide entfernen

**Files:**
- Modify: `slides.qmd` — Slide "## Dokumentierte Unterrichtspraxis — Internationale Fallauswahl" (Zeile 285 aktuell) vollständig entfernen

Begründung: Mollick, Kentz, Haverkamp, Roberts, Oxford, iArgue kommen in den Phasen-Slides inhaltlich zurück. Die Weltreise ist Name-Dropping ohne didaktische Notwendigkeit.

- [ ] **Step 1: Slide-Block entfernen**

Suche `## Dokumentierte Unterrichtspraxis — Internationale Fallauswahl` und lösche alles bis zur nächsten `## `-Überschrift (vermutlich `## Phase 1: Planen · Blume · Mollick · Kentz`).

Verwende Edit-Tool mit gesamtem Block als `old_string` und leerem `new_string` (bzw. einer einzelnen Leerzeile).

- [ ] **Step 2: Verifikation**

```bash
grep -c "^## Dokumentierte Unterrichtspraxis" slides.qmd
grep -c "globe-tile" slides.qmd
```

Erwartung: beide `0` (alle Weltreise-Referenzen entfernt).

---

## Task 6: Phase-Slides zusammenführen (4×2 → 4×1)

Jede Phase bekommt nur noch **eine** Slide, die Workflow UND Forschungs-Abbildung nebeneinander zeigt.

**Files:**
- Modify: `slides.qmd` — acht Phasen-Slides (4 Workflow + 4 Empirie) werden zu vier Kombi-Slides zusammengeführt

### Task 6.1: Phase 1 Planen (Workflow + Schneegaß)

- [ ] **Step 1: Beide Phase-1-Slides mit Merge-Slide ersetzen**

Ersetze den Bereich von `## Phase 1: Planen · Blume · Mollick · Kentz` bis zum Beginn von `## Phase 2: Strukturieren · UNC · Oxford · PHZH iArgue` mit:

```markdown
## Phase 1 · Planen — Blume · Mollick · Kentz

<div class="workflow" style="margin-top: 0.3em;">
<div class="wf-step analog">
<div class="wf-label">1 · Analog · <a href="https://bobblume.de/2025/01/05/unterricht-vorbereitung-fuer-die-klausur-parabelinterpretation/" target="_blank">nach Bob Blume</a></div>
<div class="wf-title">Strukturiertes Vorwissen zuerst</div>
<div class="wf-detail">Drei Schritte vor jeder KI: Problem identifizieren · Gliederung skizzieren · eigene Frage formulieren.</div>
</div>
<div class="arrow">→</div>
<div class="wf-step ki">
<div class="wf-label">2 · KI · <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4475995" target="_blank">nach Ethan Mollick</a></div>
<div class="wf-title">KI als Tutor, nicht als Autor</div>
<div class="wf-detail">"<em>Act as a tutor. Ask me 5 increasingly difficult questions. Do not give answers — only questions.</em>"</div>
</div>
<div class="arrow">→</div>
<div class="wf-step analog">
<div class="wf-label">3 · Analog · <a href="https://mikekentz.substack.com/p/what-happened-when-we-taught-ai-literacy" target="_blank">nach Mike Kentz</a></div>
<div class="wf-title">Chat-Transkript annotieren</div>
<div class="wf-detail"><span style="color:#e30059;">rot</span> übernommen · <span style="color:#7a00df;">lila</span> verworfen · <span style="color:#2b6cb0;">blau</span> eigener Gedanke.</div>
</div>
</div>

<div style="display: grid; grid-template-columns: 1fr 1.2fr; gap: 1.2rem; margin-top: 1em; align-items: center;">

<div>
<a class="linked-img" href="https://xn--leserume-4za.de/wp-content/uploads/2025/06/Schneegass-2025-LR-JG12-H11.pdf" target="_blank">
<img src="images/literature-figures/schneegass-dokumentenportraits.png" style="width: 100%;" alt="Dokumentenportraits">
</a>
<p class="credit"><a href="https://xn--leserume-4za.de/wp-content/uploads/2025/06/Schneegass-2025-LR-JG12-H11.pdf" target="_blank">Schneegaß (2025)</a> · reale Schüler:innen-Schreibprozesse (grün = ChatGPT)</p>
</div>

<div class="evidence" style="margin: 0;">
<div class="evidence-label">Empirisch · Sekundarstufe</div>
<div class="evidence-text">Sek-Lernende nutzen ChatGPT <strong>am häufigsten beim Planen</strong>, kaum beim Überarbeiten.</div>
<div class="evidence-source"><a href="https://doi.org/10.1002/jaal.1373" target="_blank">Levine et al. (2025)</a>, JAAL 68(5).</div>
</div>

</div>
```

### Task 6.2: Phase 2 Strukturieren (Workflow + Philipp iArgue)

- [ ] **Step 1: Beide Phase-2-Slides mergen**

Ersetze den Bereich von `## Phase 2: Strukturieren · UNC · Oxford · PHZH iArgue` bis `## Phase 3: Formulieren · Wampfler · LSE · Roberts` mit:

```markdown
## Phase 2 · Strukturieren — UNC · Oxford · PHZH iArgue

<div class="workflow" style="margin-top: 0.3em;">
<div class="wf-step analog">
<div class="wf-label">1 · Analog · <a href="https://writingcenter.unc.edu/tips-and-tools/generative-ai-in-academic-writing/" target="_blank">nach UNC Writing Center</a></div>
<div class="wf-title">Argumente händisch gewichten</div>
<div class="wf-detail">Post-its mit allen Argumenten — <strong>vor</strong> KI-Konsultation markieren: stark · mittel · schwach.</div>
</div>
<div class="arrow">→</div>
<div class="wf-step ki">
<div class="wf-label">2 · KI · <a href="https://www.ctl.ox.ac.uk/ai-tools-in-teaching" target="_blank">nach Oxford CTL</a></div>
<div class="wf-title">Struktur-Varianten generieren</div>
<div class="wf-detail">"<em>Outline this topic as (1) argumentative, (2) descriptive, (3) expository, (4) narrative essay. Compare how priority changes.</em>"</div>
</div>
<div class="arrow">→</div>
<div class="wf-step analog">
<div class="wf-label">3 · Analog · <a href="https://xn--leserume-4za.de/wp-content/uploads/2025/06/Philipp-et-al-2025-LR-JG12-H11-1.pdf" target="_blank">nach Philipp et al., PHZH iArgue</a></div>
<div class="wf-title">Divergent → konvergent</div>
<div class="wf-detail">KI darf <strong>divergent</strong> sein — die <strong>konvergente</strong> Entscheidung verantwortet die Person schriftlich.</div>
</div>
</div>

<div style="display: grid; grid-template-columns: 1fr 1.2fr; gap: 1.2rem; margin-top: 1em; align-items: center;">

<div>
<a class="linked-img" href="https://xn--leserume-4za.de/wp-content/uploads/2025/06/Philipp-et-al-2025-LR-JG12-H11-1.pdf" target="_blank">
<img src="images/literature-figures/philipp-iargue.png" style="width: 100%;" alt="iArgue Designprinzipien">
</a>
<p class="credit"><a href="https://xn--leserume-4za.de/wp-content/uploads/2025/06/Philipp-et-al-2025-LR-JG12-H11-1.pdf" target="_blank">Philipp et al. (2025)</a> · iArgue-Designprinzipien (PHZH)</p>
</div>

<div style="font-size: 0.87em; line-height: 1.55;">
<strong>iArgue-Kernbefunde</strong> für argumentatives Schreiben:
<ul style="margin-top: 0.3em;">
<li><strong>Divergentes Denken</strong> gezielt durch KI erweitern</li>
<li><strong>Konvergentes Denken</strong> in der Textredaktion vom Menschen</li>
<li><strong>Metareflexion</strong> über KI-Output als Lernziel</li>
</ul>
<p style="margin-top: 0.5em; font-size: 0.92em; color: #4a4a4a;">Übertragbar auf Leserbrief, Stellungnahme, Fachberichte Pflege/Betreuung.</p>
</div>

</div>
```

### Task 6.3: Phase 3 Formulieren (Workflow + Freinhofer PCRR)

- [ ] **Step 1: Beide Phase-3-Slides mergen**

Ersetze `## Phase 3: Formulieren · Wampfler · LSE · Roberts` bis `## Phase 4: Überarbeiten · Haverkamp · Mollick · Kentz` mit:

```markdown
## Phase 3 · Formulieren — Wampfler · LSE · Roberts

<div class="workflow" style="margin-top: 0.3em;">
<div class="wf-step analog">
<div class="wf-label">1 · Analog · <a href="https://schulesocialmedia.com/2024/03/25/ki-als-spiegel/" target="_blank">nach Philippe Wampfler</a></div>
<div class="wf-title">Freewriting zuerst</div>
<div class="wf-detail">"<em>Erst wenn Sie wissen, was Sie sagen wollen, ist KI als Variationswerkzeug hilfreich.</em>"</div>
</div>
<div class="arrow">→</div>
<div class="wf-step ki">
<div class="wf-label">2 · KI · <a href="https://blogs.lse.ac.uk/highereducation/2022/09/07/transforming-the-classroom-with-ai/" target="_blank">nach LSE (dokumentiert)</a></div>
<div class="wf-title">Stil-Varianten + Reflexion</div>
<div class="wf-detail">"<em>Suggest style improvements while keeping my argument. Then write a reflective paragraph comparing both versions.</em>"</div>
</div>
<div class="arrow">→</div>
<div class="wf-step analog">
<div class="wf-label">3 · Analog · <a href="https://www.edutopia.org/article/ai-writing-feedback-students/" target="_blank">nach Jen Roberts</a></div>
<div class="wf-title">3-Spalten-Urteil</div>
<div class="wf-detail"><strong>Strengths</strong> · <strong>Areas of Growth</strong> · <strong>Wonderings</strong> — übernommen nur bei ≥ 2 Strengths.</div>
</div>
</div>

<div style="display: grid; grid-template-columns: 1fr 1.2fr; gap: 1.2rem; margin-top: 1em; align-items: center;">

<div>
<a class="linked-img" href="https://doi.org/10.21243/mi-01-25-26" target="_blank">
<img src="images/literature-figures/freinhofer-pcrr-framework.png" style="width: 100%;" alt="PCRR Framework">
</a>
<p class="credit"><a href="https://doi.org/10.21243/mi-01-25-26" target="_blank">Freinhofer et al. (2025)</a> · PCRR-Framework (PH Tirol)</p>
</div>

<div style="font-size: 0.87em; line-height: 1.55;">
<strong>PCRR</strong>: Plan — Create — Review — Reflect.
<p style="margin-top: 0.5em;">Ein pädagogischer Prompting-Rahmen, iterativ in drei Praxisfällen erprobt. Statt "einfach prompten" eine bewusste Phasen-Struktur, die auch Lernenden vermittelbar ist.</p>
<div class="evidence" style="margin-top: 0.6em;">
<div class="evidence-text" style="font-size: 0.92em;">"Prompt Literacy ist ein eigenständiges Lernziel, nicht bloss eine Technik." — <a href="https://doi.org/10.1002/jaal.70020" target="_blank">Tour &amp; Zadorozhnyy (2025)</a></div>
</div>
</div>

</div>
```

### Task 6.4: Phase 4 Überarbeiten (Workflow + Rezat + Alnemrat)

- [ ] **Step 1: Beide Phase-4-Slides mergen**

Ersetze `## Phase 4: Überarbeiten · Haverkamp · Mollick · Kentz` bis `## Phase 4: Adaptives KI-Feedback — ArguaTutor` ... plus den ArguaTutor-Slide bis zum nächsten `## ` (Prüfung & Datenschutz) mit:

```markdown
## Phase 4 · Überarbeiten — Haverkamp · Mollick · Kentz

<div class="workflow" style="margin-top: 0.3em;">
<div class="wf-step analog">
<div class="wf-label">1 · Peer · <a href="https://the-decoder.de/ein-lehrer-laesst-ki-bei-klassenarbeiten-zu-das-hat-er-dabei-gelernt/" target="_blank">nach Haverkamp</a></div>
<div class="wf-title">Peer liest laut vor</div>
<div class="wf-detail">"<em>Der Mund erkennt Brüche, die das Auge überliest.</em>" Stolperstellen rot markieren vor jeder KI-Nutzung.</div>
</div>
<div class="arrow">→</div>
<div class="wf-step ki">
<div class="wf-label">2 · KI · <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4475995" target="_blank">nach Mollick (Tutor-Rolle)</a></div>
<div class="wf-title">Sokratische Fragen</div>
<div class="wf-detail">"<em>Ask me 3 Socratic questions about my argument that I cannot easily answer. Do not correct — only question.</em>"</div>
</div>
<div class="arrow">→</div>
<div class="wf-step analog">
<div class="wf-label">3 · Allein · <a href="https://mikekentz.substack.com/p/a-new-assessment-design-framework" target="_blank">nach Kentz</a></div>
<div class="wf-title">Transkript-Annotation</div>
<div class="wf-detail">Chat-Transkript wird nach Rubric bewertet. <em>Wo habe ich kapituliert?</em></div>
</div>
</div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1em;">

<div>
<a class="linked-img" href="https://xn--leserume-4za.de/wp-content/uploads/2025/06/Rezat-et-al-2025-LR-JG12-H11.pdf" target="_blank">
<img src="images/literature-figures/rezat-arguatutor.png" style="width: 100%;" alt="ArguaTutor">
</a>
<p class="credit"><a href="https://xn--leserume-4za.de/wp-content/uploads/2025/06/Rezat-et-al-2025-LR-JG12-H11.pdf" target="_blank">Rezat et al. (2025)</a> · ArguaTutor (DFG-Projekt Argue)</p>
</div>

<div>
<a class="linked-img" href="https://doi.org/10.3389/feduc.2025.1614673" target="_blank">
<img src="images/literature-figures/alnemrat-deskriptive-gruppenvergleich.png" style="width: 100%;" alt="Alnemrat Gruppenvergleich">
</a>
<p class="credit"><a href="https://doi.org/10.3389/feduc.2025.1614673" target="_blank">Alnemrat et al. (2025)</a> · Pre/Post/Gain × AI vs. Lehrperson × Sprachniveau</p>
</div>

</div>
```

- [ ] **Step 2: Render + Screenshot für alle 4 Phase-Slides**

```bash
export PATH="$HOME/tools/bin:$PATH"
quarto render slides.qmd --to revealjs 2>&1 | tail -3
for i in 5 6 7 8; do
  "$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars --screenshot="_check/rf/p$(printf '%d' $i).png" --window-size=1280,720 --virtual-time-budget=4000 "file://$(pwd)/_output/slides.html#/$i" 2>/dev/null
done
```

---

## Task 7: Prüfung-Slide nach vorn (vor Phase 1) verschieben — STORNIERT

Nach erneuter Überlegung: Prüfung & Datenschutz ist am stärksten **direkt vor Hands-on**, weil dort die Verbindung zu konkreter Handlung am besten ist. Wenn sie VOR den Phasen kommt, überfrachtet sie den Einstieg.

**Aktueller Platz bleibt** — zwischen Phase 4 und Hands-on. Keine Änderung nötig.

---

## Task 8: Synthese mit expliziter Leitfragen-Rückkehr

**Files:**
- Modify: `slides.qmd` — Slide "## Synthese — drei didaktische Leitsätze" überarbeiten

Die Synthese greift nun die drei Eingangs-Fragen aus Slide 4 explizit auf (dramaturgische Klammer).

- [ ] **Step 1: Synthese-Block ersetzen**

Suche `## Synthese — drei didaktische Leitsätze` bis zur nächsten `## `-Überschrift. Ersetze mit:

```markdown
## Drei Antworten auf drei Fragen

<div style="margin-top: 0.4em; font-size: 0.88em; color: #666; font-style: italic;">
Die drei Leitfragen aus Slide 4 — und was ich Ihnen darauf antworten kann.
</div>

<div style="display: grid; grid-template-columns: auto 1fr; gap: 0.8rem 1.2rem; margin-top: 1.2em; font-size: 0.95em; line-height: 1.55;">

<div style="font-weight: 700; color: #e30059; font-size: 1.4em; text-align: right;">1</div>
<div>
<div style="font-weight: 600; color: #7a00df;">Welche Forschungsevidenz ist handlungsleitend?</div>
<div style="margin-top: 0.3em;">KI wirkt bei <strong>didaktischer Einbettung</strong> — aber mit messbarem Preis: "Individuell kreativer, kollektiv einförmiger, kognitiv kapitulierend."</div>
</div>

<div style="font-weight: 700; color: #e30059; font-size: 1.4em; text-align: right;">2</div>
<div>
<div style="font-weight: 600; color: #7a00df;">Wie kombinieren Lehrpersonen konkret?</div>
<div style="margin-top: 0.3em;">Immer im Muster <strong>analog → KI → analog</strong>. Die KI-Rolle wird bewusst gewählt: Tutor (Fragen) · Partner (Varianten) · niemals Ghostwriter.</div>
</div>

<div style="font-weight: 700; color: #e30059; font-size: 1.4em; text-align: right;">3</div>
<div>
<div style="font-weight: 600; color: #7a00df;">Drei Entscheidungen vor Montag?</div>
<div style="margin-top: 0.3em;">Prüfungsformat adaptieren (Prompt-Protokoll + mündliche Verteidigung) · Datenschutz wahren (CH/EU-gehostete Oberflächen) · Klassenregel mit Lernenden aushandeln.</div>
</div>

</div>

<div style="margin-top: 1.5em; text-align: center; font-size: 1.2em; font-style: italic; color: #e30059;">
"Prompt-Kompetenz ist ein Lernziel — keine Abkürzung."
</div>
```

- [ ] **Step 2: Rendern + Screenshot**

```bash
export PATH="$HOME/tools/bin:$PATH"
quarto render slides.qmd --to revealjs 2>&1 | tail -3
"$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars --screenshot="_check/rf/synthese.png" --window-size=1280,720 --virtual-time-budget=4000 "file://$(pwd)/_output/slides.html#/11" 2>/dev/null
```

---

## Task 9: Materialien + Claude Desktop + Repo in ein Slide mergen

**Files:**
- Modify: `slides.qmd` — Slides "## Weiterführende Materialien" und "## Wo Sie Claude selbst ausprobieren" zusammenführen

- [ ] **Step 1: Beide End-Slides durch Merge ersetzen**

Suche `## Weiterführende Materialien` bis zum Beginn von `## Literatur (Auswahl 2025/26, APA 7)`. Ersetze mit:

```markdown
## Materialien · Tools · Repo

<div style="display: grid; grid-template-columns: 1.3fr 1fr; gap: 1.5rem; margin-top: 0.6em;">

<div style="font-size: 0.9em; line-height: 1.55;">
<strong>Im Repo</strong> (QR →):
<ul style="margin-top: 0.4em; list-style: none; padding: 0;">
<li>📋 Cheat-Sheet A4 · 4 Phasen · 4 Workflows</li>
<li>✍️ Prompt-Sammlung · 12 getestete Prompts für ABU</li>
<li>📄 Schülertext Mira Imhof · Hands-on-PDF</li>
<li>📚 60 Literatur-Quellen 2025/26 · APA 7</li>
<li>🎨 Slides als HTML &amp; PDF</li>
</ul>

<div style="margin-top: 1.2em; padding: 0.8rem 1rem; background: #f4f4f2; border-radius: 8px; border-left: 3px solid #e30059;">
<strong style="color: #e30059;">Claude selbst ausprobieren</strong><br>
<a href="https://claude.ai/download" target="_blank">claude.ai/download</a> · Desktop-App für Mac &amp; Windows · kostenfreier Tarif verfügbar.
</div>

<div style="margin-top: 0.9em; font-size: 0.8em; color: #888; font-style: italic;">
github.com/ramonfueglister/picts_intensivwoche_2026
</div>
</div>

<div style="text-align: center; padding: 1rem; background: #f4f4f2; border-radius: 12px;">
<div style="font-size: 4.5em; color: #e30059; line-height: 1; font-family: monospace;">⬛⬜⬛<br>⬜⬛⬜<br>⬛⬜⬛</div>
<div style="font-size: 0.75em; color: #666; margin-top: 0.4em;">QR-Code zum Repo</div>
</div>

</div>
```

- [ ] **Step 2: Rendern + Verifikation**

```bash
export PATH="$HOME/tools/bin:$PATH"
quarto render slides.qmd --to revealjs 2>&1 | tail -3
"$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars --screenshot="_check/rf/materialien.png" --window-size=1280,720 --virtual-time-budget=4000 "file://$(pwd)/_output/slides.html#/12" 2>/dev/null
```

---

## Task 10: README und Gesamtverifikation

**Files:**
- Modify: `README.md` — Dramaturgie-Tabelle und Slide-Count aktualisieren

- [ ] **Step 1: README-Dramaturgie-Tabelle ersetzen**

Finde in `README.md` die Tabelle unter `## 🏗 Aufbau der Präsentation` und ersetze durch:

```markdown
## 🏗 Aufbau der Präsentation (15 Slides · 30 Min.)

Dramaturgie: **Problem → Frage → Vier Phasen → Montag → Abschluss**

| Min. | Slide | Inhalt |
|---|---|---|
| 00:00–00:40 | 1 | Titel |
| 00:40–01:20 | 2 | Kunstwerk-Animation (Tri-System, Cognitive Surrender) |
| 01:20–04:20 | 3 | Problem: KI kann mehr + kostet mehr (Doshi&Hauser + Shaw&Nave + Sanz-Tejeda) |
| 04:20–05:20 | 4 | Drei Leitfragen + Handzeichen-Erhebung |
| 05:20–07:20 | 5 | Vier Phasen, ein Prinzip (Hayes&Flower + Analog-first) |
| 07:20–11:20 | 6 | Phase 1 Planen (Blume/Mollick/Kentz + Schneegaß) |
| 11:20–15:20 | 7 | Phase 2 Strukturieren (UNC/Oxford/iArgue + Philipp) |
| 15:20–19:20 | 8 | Phase 3 Formulieren (Wampfler/LSE/Roberts + Freinhofer) |
| 19:20–23:20 | 9 | Phase 4 Überarbeiten (Haverkamp/Mollick/Kentz + Rezat/Alnemrat) |
| 23:20–25:20 | 10 | Drei Entscheidungen vor Montag (Prüfung/Datenschutz/Klassenregel) |
| 25:20–28:20 | 11 | Anwendungsphase · Fallarbeit |
| 28:20–29:20 | 12 | Drei Antworten auf drei Fragen (Rückkehr zu Slide 4) |
| 29:20–29:50 | 13 | Materialien · Claude Desktop · Repo |
| 29:50–30:00 | 14 | Literatur |
| Anschluss | 15 | Diskussion |
```

- [ ] **Step 2: Gesamt-Render + Slide-Count**

```bash
cd /Users/ramonfuglister/Desktop/Coding/picts_input
export PATH="$HOME/tools/bin:$PATH"
quarto render slides.qmd --to revealjs 2>&1 | tail -3
grep -c "^## " slides.qmd
grep -c "<section" _output/slides.html
```

Erwartung: 14 H2-Headings (15 - 1 für Artwork mit `##{…}`) und 16 `<section>` (inkl. Title + Artwork + 14 Content + ggf. Container).

- [ ] **Step 3: Komplette visuelle Durchprobe aller Slides**

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p _check/rf-final && rm -f _check/rf-final/*.png
for i in $(seq 0 14); do
  "$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars --screenshot="_check/rf-final/s$(printf '%02d' $i).png" --window-size=1280,720 --virtual-time-budget=4500 "file://$(pwd)/_output/slides.html#/$i" 2>/dev/null
done
ls _check/rf-final/
```

Read-Tool auf 5 Schlüssel-Slides: s02 (Problem-Merge), s03 (Drei Fragen), s04 (Vier Phasen + Prinzip), s08 (Phase 4 merged), s11 (Synthese-Rückkehr).

---

## Task 11: Commit & Push

- [ ] **Step 1: Git-Commit**

```bash
cd /Users/ramonfuglister/Desktop/Coding/picts_input
git add -A
git commit -m "$(cat <<'EOF'
Refactor: radikaler roter-Faden-Umbau · 24 → 15 Slides

Drei-Akte-Dramaturgie etabliert:
  Akt I Problem · Akt II Frage · Akt III Vier Phasen
  · Akt IV Montag · Akt V Abschluss

Merges:
- Doshi&Hauser + Shaw&Nave + Sanz-Tejeda PRISMA
  → eine Problem-Slide "Was Sie eben gesehen haben..."
- 4-Phasen-Rahmen + Analog-first-Prinzip
  → eine Slide "Vier Phasen, ein Prinzip"
- Workflow + Empirie je Phase (4×2 → 4×1)

Entfernt:
- Empirische-Befundlage-5-Evidenzen-Slide (redundant mit Problem-Slide)
- Weltreise-8-Tiles-Slide (Namen kommen in Phasen zurück)
- Claude-Desktop-Einzelslide (in Materialien integriert)

Neu:
- Ausgangslage mit 3 expliziten Leitfragen als Spanne
- Synthese "Drei Antworten auf drei Fragen" mit expliziter
  Rückkehr zu Slide 4 (dramaturgische Klammer)

Alle Quellenangaben und echten Literatur-Figuren bleiben erhalten.
Keine erfundenen Charts.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
git push origin main
```

---

## Self-Review

**Spec-Abdeckung (User-Feedback adressiert?):**

| User-Kritik | Task |
|---|---|
| "roter Faden fehlt" | Task 1+2+4+6+8+9 — narrativer Drei-Akte-Aufbau |
| "alles nochmals anschauen" | Ultrakritische Diagnose-Tabelle oben, 24→15 |
| "ultrathink" | Radikale Reduktion, keine Kosmetik |

**Platzierung einzelner Inhalte:**

| Inhalt | Wo jetzt | Wo vorher |
|---|---|---|
| Doshi & Hauser | Slide 3 Problem | Slide 3 allein |
| Shaw & Nave | Slide 3 Problem | Slide 4 allein |
| Sanz-Tejeda PRISMA | Slide 3 Problem | Slide 6 allein |
| Analog-first-Prinzip | Slide 5 (+ 4-Phasen) | Slide 8 allein |
| Weltreise | entfällt | Slide 9 |
| Empirische Befundlage (5 Evidenzen) | entfällt (reduziert auf 3 in Slide 3) | Slide 6 |
| Phase-Empirie (Schneegaß/Philipp/Freinhofer/Rezat) | Slides 6–9 (in Phase-Slides integriert) | Slides 11/13/15/17 |
| Prüfung & Datenschutz | Slide 10 (unverändert) | Slide 18 |
| Synthese Rückbezug | Slide 12 (NEU mit Leitfragen-Klammer) | Slide 20 ohne Rückbezug |
| Claude Desktop | Slide 13 integriert | Slide 22 allein |

**Placeholder-Scan:** Keine TBD, keine Auslassungen. Jeder Code-Block ist vollständig mit HTML + Quellenverweisen.

**Typ-Konsistenz:** Alle CSS-Klassen (`.workflow`, `.wf-step`, `.evidence`, `.linked-img`, `.credit`, `.fragment`) bestehen bereits im Theme. Keine neuen Klassen nötig.

**Risiken:** Task 4 mergt zwei Slides mit unterschiedlichen Layouts — der neue Kombi-Slide ist dichter als beide Einzelslides. Wenn visuell überfrachtet: split wieder in zwei Slides.

**Nicht-Ziele:** Keine Änderungen am Kunstwerk-Animation-SCSS, keine neuen Literatur-Quellen, keine Tonfall-Revision (bereits erledigt).
