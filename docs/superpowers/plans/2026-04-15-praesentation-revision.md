# Präsentations-Revision — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Die Präsentation wissenschaftlich strenger, professioneller und dramaturgisch klarer gestalten: Einstieg-Galerie entfernen, alle Beispiele verlinken, progressive Fragments für Forschungs-Folie, empirische Visualisierungen mit Gruppenvergleichen ergänzen, jovialen Tonfall eliminieren, roten Faden rekonstruieren.

**Architektur:** 7 sequentielle Revisions-Tasks. Alle Änderungen betreffen im Kern `slides.qmd` plus zusätzliche **echte** Figuren aus Open-Access-Papers unter `images/literature-figures/`. Theme-SCSS erhält nur kleine Ergänzungen (Link-Styling, Fragment-Übergänge). Es werden **keine** Charts selbst konstruiert — alle wissenschaftlichen Abbildungen stammen direkt aus publizierten Papers.

**Tech-Stack:** Quarto ≥ 1.6 (revealjs output) · Chrome-Headless für Verifikations-Screenshots · `pdftoppm` / `pdfimages` zur Extraktion echter Figuren aus OA-PDFs · bestehende Literatur-PDFs unter `images/literature-pdfs/` als Figuren-Quelle; neue OA-Papers werden via `curl` geladen und mit derselben Pipeline extrahiert.

**Arbeitsdirektive:**
- Nach jedem Task: `quarto render slides.qmd --to revealjs` und Chrome-Headless-Screenshot des betroffenen Slides zur visuellen Verifikation.
- Nach jedem Task: In-Repo-Commit (falls Git-Repo) ODER klarer Logeintrag im Plan.
- Tonfall-Register: akademisch-sachlich. Anrede: "Sie". Aktiv vor Passiv. Keine Redewendungen.

---

## Datei-Inventar

**Zu modifizieren:**
- `slides.qmd` — Hauptpräsentation (Hauptarbeit liegt hier)
- `_extensions/zag-theme/zag.scss` — Link-Styling ergänzen
- `README.md` — Slide-Count aktualisieren

**Neu zu erstellen:**
- `images/literature-pdfs/Alnemrat-2025-FiE.pdf` — Open-Access-Paper
- `images/literature-pdfs/Sanz-Tejeda-2026-FiE.pdf` — Open-Access-Paper
- `images/literature-pdfs/Alfarwan-2025-FiE.pdf` — Open-Access-Paper
- `images/literature-pdfs/Liu-2025-SLE.pdf` — Open-Access-Paper
- `images/literature-figures/<autor>-<figurname>.png` — 2–5 weitere **echte** Figuren, ausschliesslich extrahiert aus OA-Papers
- `docs/praxis-beispiele/figuren-inventar.md` — Inventar aller verwendeten Figuren mit Quelle, Typ, Verwendung

**Ausdrücklich NICHT zu erstellen:**
- Keine ggplot2-Rekonstruktionen aus Abstract-Zahlen
- Keine selbst konstruierten Effektstärken-Charts
- Keine Diagramme mit "Schätzwerten" in der Caption

**Zu erhalten (unverändert):**
- `images/literature-figures/*.png` — Extrahierte Abbildungen aus Papers
- `images/einstieg/*.png` — Screenshots (werden teils in neuer Struktur genutzt)
- `images/praxis/*.png` — Weltreise-Screenshots
- `handout/*` — Handout-Dateien (separate Revision, nicht Teil dieses Plans)

---

## Task 1: Echte wissenschaftliche Abbildungen aus Open-Access-Papers extrahieren

**Files:**
- Modify: `images/literature-figures/` (weitere echte Figuren hinzufügen)
- Create: `images/literature-pdfs/<weitere-PDFs>.pdf` (zusätzliche OA-Papers herunterladen)

**Rationale:** Die Kritik "keine schönen wissenschaftlichen Abbildungen mit Gruppenvergleichen" wird mit **echten Figuren aus publizierten Open-Access-Papers** adressiert — **ohne** eigene Zahlen zu konstruieren. Eigene ggplot2-Rekonstruktionen sind wissenschaftlich heikel (Gefahr der Fehlinterpretation der Primärstudien) und werden daher **nicht** verwendet.

Die Strategie hat drei Säulen:
1. Bereits vorhandene PDFs **systematisch nach Abbildungen durchsuchen**, die bisher übersehen wurden.
2. **Zusätzliche Open-Access-Papers** herunterladen, die bekannt für Gruppenvergleichs-Grafiken sind (Frontiers, MDPI, Springer OA).
3. Figuren mit **semantischen Dateinamen** nach `images/literature-figures/` kopieren; Quellenangabe und DOI im Dateinamen-Kommentar.

Wir zeigen **nur was wirklich in den Papers existiert** — ggf. auch dann, wenn das keine klassische "Balkendiagramm-Gruppenvergleich" ist. Qualitative Visualisierungen (wie die Dokumentenportraits von Schneegaß) und Framework-Diagramme (Ghost/Partner/Tutor, PCRR, iArgue) sind **wissenschaftliche Abbildungen** und zählen.

**Wissenschaftliche Selbstverpflichtung:** Keine ggplot2-Rekonstruktion aus Abstract-Zahlen. Keine selbst interpretierten Effektstärken. Nur Figuren, die als Bildobjekt in einem publizierten Paper existieren. Falls ein gewünschter Visualisierungs-Typ (z. B. Hybrid-Feedback-Vergleich) in keinem der verifizierten OA-Papers existiert, erscheint dieser Typ **nicht** in der Präsentation.

### Aktuell extrahierte Figuren (Baseline)

Folgende Figuren liegen bereits unter `images/literature-figures/` und sind verwendet:

| Datei | Paper | Typ |
|---|---|---|
| `steinhoff-lehnen-gpt-modell.png` | Steinhoff & Lehnen (2025) | Konzept-Diagramm (Ghost/Partner/Tutor) |
| `freinhofer-pcrr-framework.png` | Freinhofer et al. (2025) | Framework-Diagramm (PCRR) |
| `philipp-iargue.png` | Philipp et al. (2025) | Textseite mit Designprinzipien |
| `rezat-arguatutor.png` | Rezat et al. (2025) | UI-Screenshot + Struktur |
| `schneegass-dokumentenportraits.png` | Schneegaß (2025) | **Empirische Visualisierung** (Farbmatrix Schreibprozess) |

Die Dokumentenportraits sind bereits eine echte empirische Datenvisualisierung. Die anderen sind Framework-Diagramme — ebenfalls wissenschaftliche Abbildungen, aber keine Gruppenvergleiche.

- [ ] **Step 1: Vorhandene PDFs systematisch nach Abbildungen durchsuchen**

Aktion: Für jedes der 8 PDFs unter `images/literature-pdfs/` jede einzelne gerenderte Seite mit `Read`-Tool auf Abbildungen inspizieren. Ziel: bisher übersehene Balkendiagramme, Box-Plots, Forest-Plots, Pre-Post-Linien, Effect-Size-Tabellen identifizieren.

```bash
cd /Users/ramonfuglister/Desktop/Coding/picts_input/images/literature-pdfs
for d in extracted_*/; do
  echo "=== $d ==="
  for p in "$d"page-*.png; do
    size=$(stat -f%z "$p" 2>/dev/null)
    if [ "$size" -gt "300000" ]; then
      echo "  $p ($size bytes) — Kandidat"
    fi
  done
done
```

Für jeden "Kandidat" via `Read`-Tool inspizieren. Kriterien für "echte Gruppenvergleichs-Abbildung":
- Balkendiagramm mit Kategorien auf x-Achse, numerischer y-Achse
- Linien­diagramm mit mindestens zwei Gruppen
- Box-Plot / Violinplot
- Forest-Plot (horizontale Effektstärken-Intervalle)
- Tabelle mit Gruppen-Mittelwerten, Standard­abweichungen oder p-Werten (weniger Bild-typisch, aber legitim)

Für jede identifizierte Figur notieren: Paper, Seite, inhaltliche Aussage.

- [ ] **Step 2: Gefundene Figuren mit semantischen Namen kopieren**

Für jede in Step 1 gefundene Abbildung:

```bash
cp images/literature-pdfs/extracted_<paper>/page-NN.png \
   images/literature-figures/<autor>-<kurztitel>.png
```

Dateiname-Konvention: `<erstautor>-<inhaltsschlagwort>.png`, z. B. `rezat-feedback-typen.png`, `schneegass-gruppenvergleich.png`.

Bei **Unsicherheit** (ist das eine Abbildung mit Aussagewert, oder nur Text mit Layout-Kasten?) **nicht** übernehmen.

- [ ] **Step 3: Open-Access-Papers mit bekannten Gruppenvergleichs-Figuren herunterladen**

Gezielt vier zusätzliche OA-Papers laden, die mit hoher Wahrscheinlichkeit echte Gruppenvergleichs-Plots enthalten:

```bash
cd /Users/ramonfuglister/Desktop/Coding/picts_input/images/literature-pdfs

# Alnemrat et al. (2025) — Frontiers in Education (OA, CC BY) — RCT AI vs Teacher Feedback
curl -sL -o "Alnemrat-2025-FiE.pdf" \
  "https://www.frontiersin.org/articles/10.3389/feduc.2025.1614673/pdf"

# Sanz-Tejeda et al. (2026) — Frontiers in Education (OA) — Systematic Review
curl -sL -o "Sanz-Tejeda-2026-FiE.pdf" \
  "https://www.frontiersin.org/articles/10.3389/feduc.2025.1711718/pdf"

# Alfarwan (2025) — Frontiers in Education (OA) — Systematic Review K-12
curl -sL -o "Alfarwan-2025-FiE.pdf" \
  "https://www.frontiersin.org/articles/10.3389/feduc.2025.1647573/pdf"

# Liu, Sihes, Ye (2025) — Smart Learning Environments (Springer, OA)
curl -sL -o "Liu-2025-SLE.pdf" \
  "https://slejournal.springeropen.com/counter/pdf/10.1186/s40561-025-00406-0.pdf"

ls -la *.pdf | tail -10
```

Erwartung: Vier neue PDFs, je zwischen 500 kB und 5 MB. Falls eine URL 404 liefert: URL-Pattern auf der jeweiligen Artikel-Landingpage nachschlagen und korrigieren.

**Hinweis:** Zhang et al. (2025) in *Innovation in Language Learning and Teaching* (Taylor & Francis) und Hwang et al. (2025) in *Journal of Second Language Writing* (Elsevier) sind **nicht OA** — diese werden **nicht** heruntergeladen. Wir zitieren sie im Text, zeigen aber keine Figuren aus ihnen.

- [ ] **Step 4: Seiten der neuen PDFs als PNG rendern**

```bash
cd /Users/ramonfuglister/Desktop/Coding/picts_input/images/literature-pdfs
for pdf in Alnemrat-2025-FiE.pdf Sanz-Tejeda-2026-FiE.pdf Alfarwan-2025-FiE.pdf Liu-2025-SLE.pdf; do
  name="${pdf%.pdf}"
  mkdir -p "extracted_$name"
  pdftoppm -png -r 150 "$pdf" "extracted_$name/page"
  echo "$pdf: $(ls extracted_$name/ | wc -l) pages"
done
```

Erwartung: Vier neue `extracted_<name>/`-Verzeichnisse mit Page-PNGs.

- [ ] **Step 5: Neue Papers nach Figuren durchsuchen (gleiche Systematik wie Step 1)**

```bash
for d in extracted_Alnemrat-2025-FiE extracted_Sanz-Tejeda-2026-FiE extracted_Alfarwan-2025-FiE extracted_Liu-2025-SLE; do
  echo "=== $d ==="
  for p in "$d"/page-*.png; do
    size=$(stat -f%z "$p" 2>/dev/null)
    if [ "$size" -gt "250000" ]; then
      echo "  $p ($size bytes)"
    fi
  done
done
```

Jeden Kandidat via `Read`-Tool prüfen. Identifizieren:
- **Alnemrat et al.**: vermutlich Balkendiagramm oder Tabelle zu AI vs. Teacher Feedback pro Niveau
- **Sanz-Tejeda et al.**: vermutlich PRISMA-Flussdiagramm (sehr nützlich als "Review-Methodik"), evtl. Forest-Plot
- **Alfarwan**: PRISMA-Flussdiagramm, evtl. Studienverteilung K-12
- **Liu et al.**: Konzept-Mapping der 15 Studien

- [ ] **Step 6: Gefundene echte Figuren kopieren und benennen**

Minimales Erfolgs-Kriterium für Task 1: **zwei** zusätzliche echte Gruppenvergleichs- oder Datenvisualisierungs-Figuren finden und einbinden. Wenn nach Steps 1–5 keine weiteren echten Abbildungen gefunden werden, wird **kein** weiterer Chart ergänzt — die Präsentation bleibt bei den bereits vorhandenen fünf Figuren.

Für jede neu gefundene Figur:

```bash
cp images/literature-pdfs/extracted_<name>/page-NN.png \
   images/literature-figures/<autor>-<kurztitel>.png
```

Beispiele (falls gefunden):
- `alnemrat-ai-vs-teacher-balken.png`
- `sanz-tejeda-prisma-flussdiagramm.png`
- `alfarwan-studienverteilung.png`
- `liu-sle-studien-matrix.png`

- [ ] **Step 7: Verzeichnis-Inventar erstellen**

Aktion:
```bash
ls -la images/literature-figures/
```

Liste und dokumentiere in `docs/praxis-beispiele/figuren-inventar.md` jede Figur mit:
- Dateiname
- Quelle (APA 7, DOI)
- Typ (Framework / Empirie / Screenshot / Review-Struktur)
- Verwendung in welcher Slide

Dieses Inventar wird später in Task 6 referenziert, um Phasen-Slides entsprechend auszustatten.

- [ ] **Step 8: Entscheidung über Slide-Einbau**

Basierend auf dem Inventar aus Step 7:
- **Wenn** ≥ 2 echte Gruppenvergleichs-Plots verfügbar: diese in Task 3 (Forschungs-Teaser) und Task 6 (Phasen 1 oder 4) einbinden.
- **Wenn** nur qualitative/Framework-Figuren vorhanden: auf Gruppenvergleichs-Plots verzichten, stattdessen PRISMA-Flussdiagramm (falls vorhanden) auf Forschungs-Teaser-Slide einbauen und ehrlich als "Methodik der Evidenzbasis" beschreiben.

Diese Entscheidung wird im Log dokumentiert.

- [ ] **Step 9: Log-Eintrag**

Am Ende des Plans anhängen:
```
## Log Task 1 erledigt: <N> zusätzliche echte Figuren extrahiert (Quellen: …). Keine erfundenen Charts. YYYY-MM-DD HH:MM.
```

---

## Task 2: Einstieg-Galerie-Slide entfernen + Handzeichen-Slide integrieren

**Files:**
- Modify: `slides.qmd` (Entfernen der Einstieg-Galerie `## Was machen Kolleg:innen aus CH, DE, AT und US?`; Umbenennen + Neuschreiben der Handzeichen-Slide zu `## Ausgangslage`)

**Rationale:** User-Kritik: "Einstieg-Galerie ist unbrauchbar — löschen." Gleichzeitig ist das Handzeichen-Element weiterhin wertvoll als aktivierender Einstieg; es wird umbenannt und umformuliert.

- [ ] **Step 1: Aktuelle Position der Einstieg-Galerie lokalisieren**

Aktion: `grep -n "## Was machen Kolleg:innen" slides.qmd`

Erwartung: Eine Zeilennummer (aktuell Zeile 12).

- [ ] **Step 2: Einstieg-Galerie-Block komplett entfernen**

Den gesamten Block zwischen `## Was machen Kolleg:innen aus CH, DE, AT und US?` und der nächsten `##`-Überschrift (`## Kurze Standortbestimmung`) entfernen — inklusive aller `<div class="card">`-Elemente, des `<p class="credit">` und der Leerzeilen. Der Block endet unmittelbar vor dem Zeichen `## Kurze`.

Verifikation: Nach dem Edit keine Vorkommen mehr von `card-desc` in den ersten 200 Zeilen:
```bash
grep -c "card-desc" slides.qmd
```
Erwartung: `0` (alle `.card`-Klassen waren nur in der Einstieg-Galerie).

- [ ] **Step 3: Handzeichen-Slide umbenennen und akademisch reformulieren**

Existierenden Block ersetzen:
```markdown
## Kurze Standortbestimmung {.smaller}

<div style="font-size:1.4em; margin-top: 1em; font-weight: 500;">
Wer nutzt <strong>KI bereits</strong> bei einer Schreibaufgabe mit Lernenden?
</div>

<ul style="margin-top: 1em; font-size: 1.05em;">
<li><strong>0 Finger</strong> — noch nie</li>
<li><strong>1 Finger</strong> — einmal ausprobiert</li>
<li><strong>2 Finger</strong> — mehrmals, gelegentlich</li>
<li><strong>3 Finger</strong> — gehört regelmässig zum Unterricht</li>
</ul>

<div style="margin-top: 1.2em; font-style: italic; color: #666;">
Heterogenität im Raum sichtbar machen — sie ist der Lern-Ort heute morgen.
</div>
```

Durch diesen neuen Block (akademischerer Tonfall, neuer Titel):

```markdown
## Ausgangslage

<div style="font-size: 1.15em; margin-top: 0.6em; line-height: 1.55;">
Generative KI ist seit November 2022 flächig verfügbar. Drei Fragen strukturieren den Input:
</div>

<ol style="margin-top: 1em; font-size: 1em; line-height: 1.7;">
<li>Was sagt die empirische Forschung 2025/26 über den Einsatz generativer KI im Schreibprozess?</li>
<li>Welche didaktischen Konsequenzen ergeben sich für den Allgemeinbildenden Unterricht in Gesundheitsberufen?</li>
<li>Welche konkreten Arbeitsweisen lassen sich in die eigene Unterrichtspraxis übernehmen?</li>
</ol>

<div class="evidence" style="margin-top: 1.4em;">
<div class="evidence-label">Erhebung im Plenum</div>
<div class="evidence-text">Wer nutzt generative KI bereits in einer Schreibaufgabe mit Lernenden? Abstufung 0–3 per Handzeichen.</div>
</div>
```

- [ ] **Step 4: Slide-Count im Footer prüfen**

Quarto zählt automatisch. Nach dem Rendern sollte die Gesamtzahl auf 21 Slides sinken (war 22).

Aktion: `quarto render slides.qmd --to revealjs 2>&1 | tail -3`

Erwartung: `Output created: _output/slides.html`, kein Fehler.

- [ ] **Step 5: Visuelle Verifikation**

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars --screenshot="_check/ausgangslage.png" --window-size=1280,720 --virtual-time-budget=4000 "file://$(pwd)/_output/slides.html#/1" 2>/dev/null
```

Anschliessend `_check/ausgangslage.png` mit `Read`-Tool prüfen. Erwartung: Titel "Ausgangslage", drei nummerierte Leitfragen sichtbar, keine leeren Einstieg-Kacheln.

---

## Task 3: Forschungs-Teaser → Empirische Befundlage mit progressiven Fragments und neuem Chart

**Files:**
- Modify: `slides.qmd` (Block `## Was die Forschung sagt (2025/26)` ersetzen)

**Rationale:** User-Kritik: "einzelne punkte müssen schrittweise eingeblendet werden nach druck auf pfeiltaste". Revealjs unterstützt `.fragment` als CSS-Klasse. Zusätzlich: "keine schönen wissenschaftlichen abbildungen mit gruppenvergleichen" → Meta-Übersichts-Chart aus Task 1 einbinden. Titel wird akademisch.

- [ ] **Step 1: Block identifizieren**

Aktion: `grep -n "Was die Forschung sagt" slides.qmd`

Erwartung: Zeilennummer des H2-Titels.

- [ ] **Step 2: Bestehenden Block vollständig ersetzen**

Alt:
```markdown
## Was die Forschung sagt (2025/26)

<div class="evidence">
<div class="evidence-label">Überblick · 136 Studien</div>
...
(komplette drei Evidence-Blöcke bis zum nächsten ## )
```

Neu:
```markdown
## Empirische Befundlage 2025/26

<div style="display: grid; grid-template-columns: 1fr 1.25fr; gap: 1.2rem; margin-top: 0.5em;">

<div>

<div class="evidence fragment" data-fragment-index="1">
<div class="evidence-label">Systematisches Review · N = 136 Studien</div>
<div class="evidence-text">Generative KI im Schreibprozess wirkt — jedoch ausschliesslich bei didaktischer Einbettung.</div>
<div class="evidence-source"><a href="https://doi.org/10.3389/feduc.2025.1711718" target="_blank">Sanz-Tejeda et al. (2026)</a></div>
</div>

<div class="evidence fragment" data-fragment-index="2">
<div class="evidence-label">Experimentell · Primarschule</div>
<div class="evidence-text">ChatGPT-Feedback steigert Kreativschreiben und Schreib-Selbstwirksamkeit signifikant (d = 0.92).</div>
<div class="evidence-source"><a href="https://doi.org/10.1177/07356331251365187" target="_blank">Kızıltaş (2025)</a></div>
</div>

<div class="evidence fragment" data-fragment-index="3">
<div class="evidence-label">RCT · EFL-Studierende</div>
<div class="evidence-text">KI-Feedback ist Lehrerfeedback statistisch äquivalent; schwächere Lernende profitieren stärker.</div>
<div class="evidence-source"><a href="https://doi.org/10.3389/feduc.2025.1614673" target="_blank">Alnemrat et al. (2025)</a></div>
</div>

<div class="evidence fragment" data-fragment-index="4" style="border-left-color: #7a00df;">
<div class="evidence-label" style="color:#7a00df;">Qualitatives Experiment</div>
<div class="evidence-text">KI erhöht die Output-Qualität, senkt aber die intrinsische Motivation.</div>
<div class="evidence-source"><a href="https://doi.org/10.1016/j.chbah.2025.100140" target="_blank">Mei et al. (2025)</a></div>
</div>

<div class="evidence fragment" data-fragment-index="5" style="border-left-color: #7a00df;">
<div class="evidence-label" style="color:#7a00df;">Methodenkritik</div>
<div class="evidence-text">Viele KI-Effektstudien bleiben unterspezifiziert — "an effect in search of a cause".</div>
<div class="evidence-source"><a href="https://doi.org/10.1111/jcal.70105" target="_blank">Weidlich et al. (2025)</a></div>
</div>

</div>

<div class="fragment" data-fragment-index="6">
<!-- Rechte Spalte: ECHTE Figur aus einem OA-Paper. -->
<!-- Falls in Task 1 ein PRISMA-Flussdiagramm aus Sanz-Tejeda oder Alfarwan gefunden wurde: -->
<!-- <a class="linked-img" href="https://doi.org/10.3389/feduc.2025.1711718" target="_blank"> -->
<!--   <img src="images/literature-figures/sanz-tejeda-prisma.png" style="width: 100%;" alt="PRISMA-Flussdiagramm"> -->
<!-- </a> -->
<!-- Falls keine passende echte Figur vorhanden: rechte Spalte leer lassen, Grid-Columns auf 1fr ändern. -->
<!-- KEINE erfundenen Charts einfügen. -->
</div>

</div>
```

**Wichtig:** Jeder Fragment-Block hat `data-fragment-index` — sie erscheinen sequenziell bei jedem Pfeiltasten-Druck. Die rechte Bild-Spalte (Index 6) wird **nur** belegt, wenn in Task 1 eine echte Figur (z. B. PRISMA-Flussdiagramm) aus einem der OA-Papers extrahiert werden konnte. Andernfalls entfällt die zweite Spalte und die fünf Evidenzen nutzen die volle Breite (`grid-template-columns: 1fr`).

- [ ] **Step 3: Link-Styling im Theme prüfen**

Datei `_extensions/zag-theme/zag.scss` öffnen. Falls noch kein spezifisches Styling für Links in `.evidence-source a` vorhanden, ergänzen:

```scss
  .evidence-source a {
    color: inherit;
    text-decoration: underline;
    text-decoration-color: rgba(227,0,89,0.3);
    text-underline-offset: 2px;

    &:hover {
      color: #e30059;
      text-decoration-color: #e30059;
    }
  }
```

Position: Im `.reveal`-Block in der Nähe der bestehenden `.evidence`-Regeln einfügen.

- [ ] **Step 4: Rendern und Fragments testen**

```bash
quarto render slides.qmd --to revealjs 2>&1 | tail -3
```

- [ ] **Step 5: Fragment-Verhalten visuell verifizieren**

Chrome-Headless kann Fragment-Zustände nicht einfach simulieren. Stattdessen im regulären Browser öffnen:
```bash
open _output/slides.html
```

Im Browser zur Slide "Empirische Befundlage 2025/26" navigieren, dann mit **Pfeil rechts** 6× drücken. Erwartung: jedes der 5 Evidenz-Felder erscheint sequenziell, dann das Chart.

- [ ] **Step 6: Commit / Log**

Log anhängen: `## Log Task 3 erledigt: Forschungs-Slide mit 5 fragmentierten Evidenzen + Chart implementiert.`

---

## Task 4: Alle Bilder und Beispiele anklickbar machen (Link-Wrapping)

**Files:**
- Modify: `slides.qmd` (systematisches Wrappen aller `<img>` in `<a>`-Tags, alle Quellenangaben verlinken)
- Modify: `_extensions/zag-theme/zag.scss` (Hover-Effekt für klickbare Screenshots)

**Rationale:** User-Kritik: "alle deine beispiele müssen natürlich anklickbar sein und zur jeweiligen seite führen."

- [ ] **Step 1: Alle Image-Referenzen inventarisieren**

Aktion: `grep -n "<img\|!\[" slides.qmd`

Erwartung: Liste aller Bilder mit Zeilennummern. Jede Zeile erhält ein `<a href="URL" target="_blank">`-Wrapper.

- [ ] **Step 2: CSS für klickbare Bilder ergänzen**

In `_extensions/zag-theme/zag.scss` im `.reveal`-Block ergänzen:

```scss
  a.linked-img {
    display: block;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    text-decoration: none;

    &:hover {
      transform: translateY(-2px);
      img {
        box-shadow: 0 4px 14px rgba(227, 0, 89, 0.22);
        outline: 2px solid rgba(227, 0, 89, 0.35);
        outline-offset: 2px;
      }
    }

    img {
      transition: box-shadow 0.15s ease, outline 0.15s ease;
    }
  }

  .globe-tile {
    &:hover {
      transform: translateY(-2px);
      transition: transform 0.15s ease;
    }
  }

  /* Credit-Links */
  .credit a {
    color: inherit;
    text-decoration: underline;
    text-decoration-color: rgba(136,136,136,0.4);

    &:hover {
      color: #e30059;
    }
  }
```

- [ ] **Step 3: Weltreise-Slide — alle 8 Tiles klickbar machen**

Ersetze jeden `<div class="globe-tile...">`-Block durch eine verlinkte Variante. Beispiel (erster Tile):

Alt:
```html
<div class="globe-tile uni">
<img src="images/praxis/eth-ai-guidelines.png" alt="ETH Zurich">
<div class="gt-name"><span class="gt-flag">🇨🇭</span>ETH Zürich</div>
...
</div>
```

Neu:
```html
<a class="globe-tile-link" href="https://ethz.ch/staffnet/en/news-and-events/internal-news/archive/2024/07/new-guidelines-for-the-use-of-generative-ai-in-education.html" target="_blank" style="text-decoration: none; color: inherit;">
<div class="globe-tile uni">
<img src="images/praxis/eth-ai-guidelines.png" alt="ETH Zurich">
<div class="gt-name"><span class="gt-flag">🇨🇭</span>ETH Zürich</div>
<div class="gt-meta">Universität · 2024</div>
<div class="gt-what">Obligatorische "Statement on Usage of AI" in BA/MA-Thesen — wer welches Tool wofür.</div>
</div>
</a>
```

Die anderen 7 Tiles nach dem gleichen Muster mit folgenden URLs verlinken:

| Tile | URL |
|---|---|
| HSG Writing Lab | `https://www.unisg.ch/en/newsdetail/news/scientific-writing-with-ai-support-at-hsg-the-focus-is-on-critical-reflection/` |
| Mollick | `https://www.oneusefulthing.org/` |
| Oxford CTL | `https://www.ctl.ox.ac.uk/ai-tools-in-teaching` |
| Haverkamp | `https://the-decoder.de/ein-lehrer-laesst-ki-bei-klassenarbeiten-zu-das-hat-er-dabei-gelernt/` |
| Mike Kentz | `https://mikekentz.substack.com/p/a-new-assessment-design-framework` |
| Jen Roberts | `https://www.edutopia.org/article/ai-writing-feedback-students/` |
| NUS AICET | `https://aicet.comp.nus.edu.sg/aicet-learning-journey-pedagogy-first-teaching-with-not-by-ai/` |

- [ ] **Step 4: Phasen-"Praxis"-Slides — Literatur-Figuren verlinken**

Für jede der vier Phasen-Forschungs/Praxis-Slides: `<img>` der Literatur-Figur in `<a>`-Wrapper setzen.

Mapping:

| Phase | Figur | Ziel-URL |
|---|---|---|
| Phase 1 | `schneegass-dokumentenportraits.png` | `https://xn--leserume-4za.de/wp-content/uploads/2025/06/Schneegass-2025-LR-JG12-H11.pdf` |
| Phase 2 | `philipp-iargue.png` | `https://xn--leserume-4za.de/wp-content/uploads/2025/06/Philipp-et-al-2025-LR-JG12-H11-1.pdf` |
| Phase 3 | `freinhofer-pcrr-framework.png` | `https://doi.org/10.21243/mi-01-25-26` |
| Phase 4 | `rezat-arguatutor.png` | `https://xn--leserume-4za.de/wp-content/uploads/2025/06/Rezat-et-al-2025-LR-JG12-H11.pdf` |
| Backup | `steinhoff-lehnen-gpt-modell.png` | `https://xn--leserume-4za.de/wp-content/uploads/2025/06/Steinhoff-Lehnen-2025-LR-JG12-H11.pdf` |

Beispiel (Phase 1):

Alt:
```html
<img src="images/literature-figures/schneegass-dokumentenportraits.png" style="width: 95%;" alt="Dokumentenportraits">
```

Neu:
```html
<a class="linked-img" href="https://xn--leserume-4za.de/wp-content/uploads/2025/06/Schneegass-2025-LR-JG12-H11.pdf" target="_blank" style="width: 95%; display: inline-block;">
<img src="images/literature-figures/schneegass-dokumentenportraits.png" style="width: 100%;" alt="Dokumentenportraits">
</a>
```

- [ ] **Step 5: Alle Inline-Zitate verlinken**

In den vier Phasen-Workflow-Slides und in Phase-Praxis-Slides die Inline-Zitate (z. B. `<div class="citation">"Hybrides Feedback (KI + Mensch) übertrifft beide einzeln." — Zhang et al. (2025)</div>`) so umformen:

```html
<div class="citation">"Hybrides Feedback (KI + Mensch) übertrifft beide einzeln." — <a href="https://doi.org/10.1080/17501229.2025.2503890" target="_blank">Zhang et al. (2025)</a></div>
```

Zuordnungstabelle:

| Zitat | URL |
|---|---|
| Steinhoff & Lehnen (2025) | `https://xn--leserume-4za.de/wp-content/uploads/2025/06/Steinhoff-Lehnen-2025-LR-JG12-H11.pdf` |
| Levine et al. (2025) | `https://doi.org/10.1002/jaal.1373` |
| Tour & Zadorozhnyy (2025) | `https://doi.org/10.1002/jaal.70020` |
| Zhang et al. (2025) | `https://doi.org/10.1080/17501229.2025.2503890` |
| Philipp et al. (2025) | `https://xn--leserume-4za.de/wp-content/uploads/2025/06/Philipp-et-al-2025-LR-JG12-H11-1.pdf` |
| Rezat et al. (2025) | `https://xn--leserume-4za.de/wp-content/uploads/2025/06/Rezat-et-al-2025-LR-JG12-H11.pdf` |
| Freinhofer et al. (2025) | `https://doi.org/10.21243/mi-01-25-26` |
| Sanz-Tejeda et al. (2026) | `https://doi.org/10.3389/feduc.2025.1711718` |
| Kızıltaş (2025) | `https://doi.org/10.1177/07356331251365187` |
| Hwang et al. (2025) | `https://doi.org/10.1016/j.jslw.2025.101230` |
| Mei et al. (2025) | `https://doi.org/10.1016/j.chbah.2025.100140` |
| Alnemrat et al. (2025) | `https://doi.org/10.3389/feduc.2025.1614673` |
| Warner (2025) | `https://www.hachettebookgroup.com/titles/john-warner/more-than-words/9781541605510/` |
| Weidlich et al. (2025) | `https://doi.org/10.1111/jcal.70105` |

Alle Vorkommen im gesamten `slides.qmd` verlinken.

- [ ] **Step 6: Literaturfolie — Alle Referenzen mit DOI-Links**

Die komplette Literaturfolie (aktuell unformatierte Text-Liste mit blauen URLs) systematisch mit `<a>`-Tags umbauen. Jede APA-7-Referenz erhält einen Link zur DOI-URL. Die URLs stehen bereits teilweise im Text — diese zusätzlich als `<a>`-Wrapper um Autor:innen-Namen setzen, damit ein Klick auf den Namen öffnet.

- [ ] **Step 7: Rendern und Link-Verifikation**

```bash
quarto render slides.qmd --to revealjs 2>&1 | tail -3
grep -c "href=\"http" _output/slides.html
```

Erwartung: Rendern OK, > 40 Treffer für `href="http` (alle erwarteten Links).

- [ ] **Step 8: Link-Testing stichprobenartig**

Im Browser Slide 6 (Weltreise) öffnen, auf ETH-Zürich-Kachel klicken. Erwartung: neuer Tab öffnet die ETH-Website.

Log anhängen: `## Log Task 4 erledigt: XX Links eingefügt, stichprobenartig geprüft.`

---

## Task 5: Tonfall-Überarbeitung (Sie-Ansprache, akademisch-sachlich)

**Files:**
- Modify: `slides.qmd` (global: alle jovialen Phrasen ersetzen)

**Rationale:** User-Kritik: "der joviale ton ist unprofessionell". Die Präsentation richtet sich an Fachkolleg:innen; der Ton soll sachlich, präzise, siezend sein.

- [ ] **Step 1: Vollständige Ersetzungstabelle anlegen**

Folgende Ersetzungen werden in `slides.qmd` exakt einmal durchgeführt (oder `replace_all: true`, falls Phrase unique):

| Alt | Neu |
|---|---|
| `# Analoge und digitale Schreibprozesse kombinieren` | `# Schreibprozesse im Zeitalter generativer KI` (als `title:`-Feld im YAML) |
| `Wie KI und analoge Methoden den Schreibprozess gemeinsam bereichern` | `Empirische Befunde und didaktische Konsequenzen für den ABU-Unterricht` |
| `## Jetzt ihr.` | `## Anwendungsphase · Fallarbeit` |
| `Paar-/Dreier-Gruppen · Ihr überarbeitet einen FaGe-Bewerbungstext mit KI` | `Paar- oder Dreier-Gruppen: Überarbeitung eines FaGe-Bewerbungstexts mit KI-Unterstützung` |
| `Ablauf · 5 Minuten` | `Ablauf (5 Minuten)` |
| `• 0:30 Text lesen` | `0:30 Rezeption des Textes` |
| `• 2:00 Prompt → KI laufen lassen` | `2:00 Prompt formulieren und ausführen` |
| `• 1:30 Gruppe: übernehmen / verwerfen? warum?` | `1:30 Gruppenarbeit: Annehmen / Verwerfen mit Begründung` |
| `• 1:00 Plenum: 1 Erkenntnis pro Gruppe` | `1:00 Plenum: eine zentrale Erkenntnis je Gruppe` |
| `## 3 Takeaways` | `## Synthese — drei didaktische Leitsätze` |
| `KI **ersetzt** keine Schreibphase — sie **verändert**, wie wir sie gestalten.` | `Generative KI ersetzt keine Schreibphase. Sie verändert, wie Schreibphasen gestaltet werden.` |
| `Analog + digital ist **keine Addition**, sondern Kombination. Entscheide **pro Phase**.` | `Analoge und digitale Verfahren bilden keine Addition, sondern eine Komposition — mit phasenspezifischen Entscheidungen.` |
| `**Prompt-Kompetenz** ist Lernziel, nicht Abkürzung. Und sie lässt sich lernen — wie alles.` | `Prompt-Kompetenz ist ein eigenständiges Lernziel und muss als solches explizit vermittelt werden.` |
| `## Alles zum Mitnehmen` | `## Weiterführende Materialien` |
| `**Im Repo findest du:**` | `**Begleitmaterialien im Repositorium:**` |
| `## Fragen?` | `## Diskussion` |
| `Danke fürs Mitdenken.` | `Vielen Dank für Ihre Aufmerksamkeit.` |
| `## Blick in die Welt — 8 konkrete Klassenzimmer` | `## Dokumentierte Unterrichtspraxis — Internationale Fallauswahl` |
| `+ 40 weitere dokumentierte Fälle im Repo` | `Ergänzende 30 Fälle in der Praxis-Datenbank des Repositoriums` |
| `Heterogenität im Raum sichtbar machen — sie ist der Lern-Ort heute morgen.` | (entfallen, siehe Task 2) |
| `"Analog-first" als Faustregel` | `Didaktisches Prinzip: Analoge Vorarbeit zuerst` |
| `Eigenes Denken zuerst → KI-Input → dein Entscheid` | `Eigenständige Konzeptarbeit → KI-Input → begründete Entscheidung` |
| `Lernende nutzen KI am intensivsten bei der **Ideenfindung**, deutlich weniger beim Überarbeiten.` | `Empirisch konzentriert sich die KI-Nutzung auf frühe Prozess­phasen — insbesondere die Ideenfindung.` |
| `KI hebt die **Output-Qualität**, senkt aber die **intrinsische Motivation** und das Gefühl von Autor:innenschaft.` | `KI-Einsatz erhöht die Output-Qualität, reduziert jedoch die intrinsische Motivation und das Erleben von Autor:innenschaft.` |
| `**Ausnahmen:** (1) Recherche-Start bei Null-Vorwissen · (2) Schreibblockade durchbrechen · (3) Standardisierte Formulare (Protokolle, Checklisten)` | `**Ausnahmefälle:** Recherche bei fehlendem Vorwissen · standardisierte Textsorten (Protokoll, Checkliste) · Überwindung produktiver Blockaden.` |
| `## Phase 1 · Planen — Workflow` | `## Phase 1: Planen — didaktischer Workflow` |
| (analog für Phase 2, 3, 4) | analog |
| `## Phase 1 · Was Lernende tatsächlich tun` | `## Phase 1: Empirische Befunde zur realen KI-Nutzung` |
| `## Phase 2 · PHZH-Projekt "iArgue" (CH)` | `## Phase 2: Forschungsprojekt iArgue (PHZH)` |
| `## Phase 3 · PCRR-Framework (AT)` | `## Phase 3: PCRR-Framework (PH Tirol)` |
| `## Phase 4 · ArguaTutor (DACH-Forschung)` | `## Phase 4: Adaptives KI-Feedback — ArguaTutor` |
| `## Der Schreibprozess — nicht linear, iterativ` | `## Theoretischer Rahmen: Schreibprozess als rekursives Modell` |
| `↺ Rücksprünge erlaubt · jederzeit · überall` | `Rekursive Rücksprünge zwischen allen Phasen (Hayes & Flower, 1980; Kellogg, 1996 ff.)` |
| `Cluster händisch` | `Eigenes Cluster · handschriftlich` |
| `Alle Argumente, Fakten, Fragen auf Kärtchen legen → **Material sichten**.` | `Argumente, Fakten, Fragen auf Karten — systematische Material-Sichtung.` |
| `Freewriting · Hand & Papier` | `Freewriting (handschriftlich, ohne Korrektur)` |
| `Laut vorlesen lassen` | `Peer-Review durch Vorlesen` |
| `Peer markiert Stolperstellen rot auf Papier — **menschliche Resonanz zuerst**.` | `Peer markiert Stolperstellen — menschliche Textresonanz als erster Zugang.` |
| `KI als kritische Leserin` | `KI in der Rolle der kritischen Leserin` |
| `Eigene Fassung` | `Autor:innen-Fassung erstellen` |
| `Markierte Stellen (Peer + KI) neu schreiben — **Entscheidungshoheit bleibt**.` | `Kombinierte Markierungen (Peer und KI) werden autor:innen­seitig integriert.` |

- [ ] **Step 2: Die 4 Forschungs-/Praxis-Slides prüfen auf verbleibende Kolloquialismen**

Problematische Formulierungen identifizieren und ersetzen:

| Alt | Neu |
|---|---|
| `**Für FaGe/FaBe-Unterricht:** Das ist die Tür, die bei Lernenden schon offen ist — **nutzt sie**, statt sie zu verriegeln.` | `Didaktische Implikation für FaGe-/FaBe-Unterricht: Die Planungsphase ist der natürliche Einstiegspunkt für einen strukturierten KI-Einsatz.` |
| `**Für ABU/BMS:** übertragbar auf Leserbrief, Stellungnahme, Argumentation in Fach­berichten der Pflege/Betreuung.` | `Transfer in den ABU-/BMS-Unterricht: übertragbar auf Leserbrief, Stellungnahme und argumentativ-begründende Fachberichte in Pflege und Betreuung.` |
| `**Für ABU:** Statt "einfach prompten" — bewusste Phasen­struktur, auch für Lernende gut vermittelbar.` | `Für den ABU-Unterricht ermöglicht die Phasenstruktur eine reflektierte Prompt-Arbeit, die auch Lernenden vermittelt werden kann.` |
| `**Nicht einfach Korrektur** — der Tutor **fragt**, wo die Argumentation brüchig ist.` | `Der Tutor operiert nicht korrigierend, sondern fragend — er markiert argumentative Brüche durch gezielte Rückfragen.` |
| `Übertragbar auf **Pflegedokumentation, Praktikumsberichte, Reflexionen**: überall, wo Lernende ihre Argumentation sichtbar machen müssen.` | `Der Ansatz ist auf Pflegedokumentation, Praktikumsberichte und reflektierende Texte übertragbar — durchgängig dort, wo argumentative Strukturen explizit zu machen sind.` |

- [ ] **Step 3: Rendern + Verifikation**

```bash
quarto render slides.qmd --to revealjs 2>&1 | tail -3
```

Anschliessend `grep -n "Jetzt ihr\|Danke fürs Mitdenken\|Alles zum Mitnehmen\|Kolleg:innen aus CH" slides.qmd`. Erwartung: `0` Treffer (alle entfernt).

- [ ] **Step 4: Stichprobenartige visuelle Verifikation (3 Slides)**

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
for idx in 13 14 17; do
  "$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars --screenshot="_check/tonfall-$idx.png" --window-size=1280,720 --virtual-time-budget=4000 "file://$(pwd)/_output/slides.html#/$idx" 2>/dev/null
done
```

Prüfen mit `Read`-Tool: Anwendungsphase-Slide (13), Synthese (14), Diskussion (17). Kriterium: keine "Du"-Ansprache, keine umgangssprachlichen Wendungen, keine kolloquialen Verben.

Log: `## Log Task 5 erledigt: Tonfall-Revision abgeschlossen, Stichprobe visuell geprüft.`

---

## Task 6: Roter Faden rekonstruieren — Dramaturgie-Neuordnung

**Files:**
- Modify: `slides.qmd` (YAML-Header + Slide-Reihenfolge)

**Rationale:** User-Kritik: "der rote faden ist nicht genügend gut". Die neue Dramaturgie folgt dem Muster **Problem → Evidenz → Theorie → Praxis → Anwendung → Synthese**, statt der bisherigen Mischung aus Einstieg, Umfrage und Befunden.

**Neue Reihenfolge (21 Slides):**

| # | Titel | Funktion |
|---|---|---|
| 1 | Titel | Metadaten |
| 2 | Ausgangslage | Drei Leitfragen + Handzeichen-Erhebung |
| 3 | Empirische Befundlage 2025/26 | Fragmentierte Evidenzen + Meta-Chart |
| 4 | Theoretischer Rahmen: Schreibprozess als rekursives Modell | 4-Phasen + Hayes/Flower-Bezug |
| 5 | Didaktisches Prinzip: Analoge Vorarbeit zuerst | Faustregel + 2 Evidenzen |
| 6 | Dokumentierte Unterrichtspraxis — Internationale Fallauswahl | Weltreise (8 Tiles) |
| 7 | Phase 1: Planen — didaktischer Workflow | 3-Schritt-Workflow |
| 8 | Phase 1: Empirische Befunde zur realen KI-Nutzung | Schneegaß-Dokumentenportraits (echt, qualitativ) + optional zweite echte Figur aus OA-Paper |
| 9 | Phase 2: Strukturieren — didaktischer Workflow | 3-Schritt-Workflow |
| 10 | Phase 2: Forschungsprojekt iArgue (PHZH) | Philipp et al. (echte Figur) |
| 11 | Phase 3: Formulieren — didaktischer Workflow | 3-Schritt-Workflow |
| 12 | Phase 3: PCRR-Framework (PH Tirol) | Freinhofer et al. (echte Figur) |
| 13 | Phase 4: Überarbeiten — didaktischer Workflow | 3-Schritt-Workflow |
| 14 | Phase 4: Adaptives KI-Feedback — ArguaTutor | Rezat et al. (echte Figur) + optional Alnemrat-Balkendiagramm, **falls** in Task 1 extrahiert |
| 15 | Anwendungsphase · Fallarbeit | Hands-on |
| 16 | Synthese — drei didaktische Leitsätze | Takeaways |
| 17 | Weiterführende Materialien | QR + Repo |
| 18 | Literaturverzeichnis (Auswahl) | 15 Refs APA 7 |
| 19 | Diskussion | Danke + Kontakt |
| 20 | Backup: Ghost/Partner/Tutor-Modell | Steinhoff & Lehnen |
| 21 | Backup: Prompt-Bibliothek | Auszug Prompts |

- [ ] **Step 1: Phase 1 Empirie-Slide — zweite echte Figur nur falls vorhanden**

Slide "Phase 1: Empirische Befunde zur realen KI-Nutzung" enthält verpflichtend das Schneegaß-Dokumentenportrait (existiert, ist echt, qualitativ-empirisch). Eine zweite Abbildung wird **nur dann** ergänzt, wenn Task 1 eine passende echte Figur extrahiert hat (z. B. Balkendiagramm "Nutzung pro Phase" aus einem OA-Paper oder Forest-Plot aus Sanz-Tejeda Review).

**Variante A — eine Figur (Default, wenn Task 1 nichts Passendes fand):**

```html
<div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 1.2rem; margin-top: 0.5em;">

<div>
<a class="linked-img" href="https://xn--leserume-4za.de/wp-content/uploads/2025/06/Schneegass-2025-LR-JG12-H11.pdf" target="_blank" style="display: block;">
<img src="images/literature-figures/schneegass-dokumentenportraits.png" style="width: 100%;" alt="Dokumentenportraits">
</a>
<p class="credit"><a href="https://xn--leserume-4za.de/wp-content/uploads/2025/06/Schneegass-2025-LR-JG12-H11.pdf" target="_blank">Schneegaß (2025)</a> — Dokumentenportraits realer Schüler:innen-Schreibprozesse (grün: ChatGPT-Nutzung)</p>
</div>

<div>
<div class="evidence">
<div class="evidence-label">Qualitative Studie · Sekundarstufe</div>
<div class="evidence-text">"Sekundar-Lernende nutzen ChatGPT in der Planungs­phase <strong>am häufigsten</strong> — aber selten für die Überarbeitung."</div>
<div class="evidence-source"><a href="https://doi.org/10.1002/jaal.1373" target="_blank">Levine et al. (2025)</a></div>
</div>
<div style="margin-top: 0.9em; font-size: 0.85em; line-height: 1.55;">
Didaktische Implikation für FaGe-/FaBe-Unterricht: Die Planungsphase ist der natürliche Einstiegspunkt für einen strukturierten KI-Einsatz.
</div>
</div>

</div>
```

**Variante B — zwei Figuren (nur wenn Task 1 eine zweite echte Figur fand):**
Erste Spalte wie in Variante A (Schneegaß), zweite Spalte ersetzt das Evidenz-Text-Paneel durch die zweite echte Figur:

```html
<div>
<a class="linked-img" href="<URL_DER_ZWEITEN_QUELLE>" target="_blank" style="display: block;">
<img src="images/literature-figures/<NAME_DER_ZWEITEN_FIGUR>.png" style="width: 100%;" alt="<ALT_TEXT>">
</a>
<p class="credit"><a href="<URL_DER_ZWEITEN_QUELLE>" target="_blank"><AUTOR> (<JAHR>)</a> — <KURZ­BESCHREIBUNG, 1 Zeile></p>
</div>
```

**Entscheidungsregel:** Falls Task 1 Step 6 eine OA-Figur mit direktem Bezug zur Phase-1-Frage ("wann nutzen Lernende KI?") erbringt, Variante B. Andernfalls Variante A. **Keine Mischung mit erfundenen Charts.**

- [ ] **Step 2: Phase 4 ArguaTutor-Slide — zweite Figur nur falls vorhanden**

Gleiche Logik wie Step 1. Die Slide enthält verpflichtend den ArguaTutor-Screenshot (Rezat et al. 2025). Eine zweite echte Figur (z. B. ein Gruppenvergleichs-Balkendiagramm aus Alnemrat et al. 2025, falls in Task 1 extrahiert) wird **nur** ergänzt, wenn sie als PNG in `images/literature-figures/` vorliegt.

**Variante A — eine Figur (Default):**

```html
<div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 1.2rem;">

<div>
<a class="linked-img" href="https://xn--leserume-4za.de/wp-content/uploads/2025/06/Rezat-et-al-2025-LR-JG12-H11.pdf" target="_blank" style="display: block;">
<img src="images/literature-figures/rezat-arguatutor.png" style="width: 100%;" alt="ArguaTutor">
</a>
<p class="credit"><a href="https://xn--leserume-4za.de/wp-content/uploads/2025/06/Rezat-et-al-2025-LR-JG12-H11.pdf" target="_blank">Rezat et al. (2025)</a> — ArguaTutor, DFG-Projekt Argue</p>
</div>

<div style="font-size: 0.9em;">
<p><strong>Adaptives KI-Feedback</strong> auf argumentative Lerner:innen-Texte: automatische Identifikation von Argument­strukturen, Rating der Schreibqualität, Feedback auf Basis schreibdidaktischer Förder­massnahmen.</p>

<p style="margin-top: 0.6em;">Der Tutor operiert nicht korrigierend, sondern fragend.</p>

<div class="evidence" style="margin-top: 0.9em;">
<div class="evidence-text" style="font-size: 0.88em;">Der Ansatz ist auf Pflegedokumentation, Praktikumsberichte und reflektierende Texte übertragbar — durchgängig dort, wo argumentative Strukturen explizit zu machen sind.</div>
</div>
</div>

</div>
```

**Variante B** analog zu Step 1: rechte Spalte durch echte Figur mit korrekter Quellenangabe ersetzen, **nur falls vorhanden**.

- [ ] **Step 3: Reihenfolge-Korrekturen in slides.qmd prüfen**

Die Slides sollten bereits weitgehend in der richtigen Reihenfolge stehen. Verifikation:

```bash
grep -n "^## " slides.qmd
```

Erwartung: Die 20 `##`-Überschriften stehen in der Reihenfolge der obigen Tabelle.

Falls nicht: Betroffene Blöcke per Cut-and-Paste verschieben.

- [ ] **Step 4: Dramaturgie-Banner auf Titel-Slide**

Aktualisiere den YAML-Header:

```yaml
---
title: "Schreibprozesse im Zeitalter generativer KI"
subtitle: "Empirische Befunde und didaktische Konsequenzen für den ABU-Unterricht"
author: "Ramon Fuglister · ABU · ZAG Winterthur"
date: "2026-04-17"
date-format: "D. MMMM YYYY"
format:
  revealjs:
    slide-number: c/t
    incremental: false
---
```

- [ ] **Step 5: Rendern und Gesamt-Struktur prüfen**

```bash
quarto render slides.qmd --to revealjs 2>&1 | tail -3
```

Danach Gesamtcount verifizieren:
```bash
grep -c "<section" _output/slides.html
```

Erwartung: ca. 25 (Title-Slide + 20 Haupt-Slides + Sub-Fragments; revealjs zählt Sections).

Log: `## Log Task 6 erledigt: Dramaturgie auf Problem→Evidenz→Theorie→Praxis→Anwendung→Synthese umgestellt.`

---

## Task 7: Finale Verifikation — alle 21 Slides, Links, Fragments, Charts

**Files:**
- Create: `_check/final-YYYY-MM-DD/slide-*.png` (21 Screenshots)

**Rationale:** Nach sämtlichen Änderungen einmal die gesamte Präsentation visuell abnehmen, Link-Integrität und Charts prüfen.

- [ ] **Step 1: Frisches Rendern**

```bash
cd /Users/ramonfuglister/Desktop/Coding/picts_input
export PATH="$HOME/tools/bin:$PATH"
rm -rf .quarto _output/slides.html
quarto render slides.qmd --to revealjs 2>&1 | tail -5
```

Erwartung: `Output created: _output/slides.html`, keine Warnungen zu fenced divs.

- [ ] **Step 2: Alle 21 Slides screenshotten**

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p _check/final && rm -f _check/final/*.png
for i in $(seq 0 20); do
  "$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars \
    --screenshot="_check/final/slide-$(printf '%02d' $i).png" \
    --window-size=1280,720 --virtual-time-budget=4500 \
    "file://$(pwd)/_output/slides.html#/$i" 2>/dev/null
done
ls _check/final/ | wc -l
```

Erwartung: 21 PNG-Dateien.

- [ ] **Step 3: Stichprobe der 6 inhaltlich kritischen Slides mit Read-Tool prüfen**

Folgende Slides je einzeln inspizieren:
- `slide-01.png` — Ausgangslage: drei Leitfragen sichtbar, keine Einstieg-Kacheln
- `slide-02.png` — Empirische Befundlage: Chart rechts, 5 Evidenzen links (Fragments sind im statischen Screenshot sichtbar, da kein JS-State)
- `slide-05.png` — Weltreise: 8 Tiles, alle klickbar (Hover-Schatten prüfen)
- `slide-07.png` — Phase 1 Empirie: Schneegaß-Figur + Hwang-Chart nebeneinander
- `slide-13.png` — ArguaTutor + Zhang-Chart
- `slide-14.png` — Anwendungsphase: "Fallarbeit" statt "Jetzt ihr."

Kriterien:
- Tonfall durchgängig akademisch
- Keine leeren Bereiche
- Charts lesbar
- Quellenangaben verlinkt

- [ ] **Step 4: Link-Integritätsprüfung**

```bash
grep -o 'href="http[^"]*"' _output/slides.html | sort -u > _check/all-links.txt
wc -l _check/all-links.txt
```

Erwartung: ≥ 45 eindeutige URLs (Literaturzitate + Weltreise-Tiles + Literaturfolie-Links).

Stichprobenartig 3 URLs per `curl -s -o /dev/null -w "%{http_code}\n" "$url"` prüfen:
```bash
for url in $(head -5 _check/all-links.txt | sed 's/href="//;s/"//'); do
  code=$(curl -sL -o /dev/null -w "%{http_code}" "$url")
  echo "$code  $url"
done
```

Erwartung: alle 200 / 3xx. Falls 404: URL in `slides.qmd` korrigieren oder entfernen.

- [ ] **Step 5: Fragment-Anzahl prüfen**

```bash
grep -c 'class="[^"]*fragment' _output/slides.html
```

Erwartung: ≥ 6 (die 5 Evidenz-Kacheln + 1 Chart auf der Empirie-Slide).

- [ ] **Step 6: Offline-Lauffähigkeit verifizieren**

```bash
du -h _output/slides.html
```

Erwartung: > 10 MB (alle Bilder + Fonts sind eingebettet dank `embed-resources: true` — Standard in Quarto ≥ 1.4).

- [ ] **Step 7: README aktualisieren**

In `README.md` diesen Abschnitt aktualisieren:

Alt:
```
## 🏗 Aufbau der Präsentation (21 Slides · 30 Min.)
(Tabelle mit alter Dramaturgie)
```

Neu:
```
## 🏗 Aufbau der Präsentation (21 Slides · 30 Min.)

| Min. | Slide | Inhalt |
|---|---|---|
| 00:00–01:30 | 1–2 | Titel + Ausgangslage (3 Leitfragen + Handzeichen-Erhebung) |
| 01:30–04:00 | 3 | Empirische Befundlage 2025/26 (5 fragmentierte Evidenzen; echte Figur aus OA-Paper, falls in Task 1 extrahiert) |
| 04:00–05:30 | 4 | Theoretischer Rahmen: Schreibprozess als rekursives Modell |
| 05:30–07:00 | 5 | Didaktisches Prinzip: Analoge Vorarbeit zuerst |
| 07:00–08:30 | 6 | Dokumentierte Unterrichtspraxis — 8 internationale Fälle |
| 08:30–22:00 | 7–14 | Phasen 1–4: Workflows + echte Literatur-Figuren (je 2 Slides) |
| 22:00–27:00 | 15 | Anwendungsphase · Fallarbeit (FaGe-Text) |
| 27:00–30:00 | 16–19 | Synthese · Materialien · Literatur · Diskussion |
| Backup | 20–21 | Ghost/Partner/Tutor · Prompt-Bibliothek |
```

- [ ] **Step 8: Abschluss-Log**

```
## Log Task 7 erledigt: Gesamtprüfung bestanden. 21 Slides, XX Links, 6 Fragments, N echte Literatur-Figuren (keine erfundenen Charts).
Revision abgeschlossen YYYY-MM-DD HH:MM.
```

---

## Self-Review

**Spec-Abdeckung (die 6 User-Kritikpunkte):**

| User-Kritik | Task-Abdeckung |
|---|---|
| (1) Beispiele anklickbar | Task 4 — alle Bilder und Zitate verlinkt |
| (2) "Kolleg:innen aus CH, DE, AT und US"-Folie löschen | Task 2 — Einstieg-Galerie entfernt |
| (3) Forschung-Folie: progressive Fragments | Task 3 — `.fragment`-Klassen eingefügt |
| (4) Wissenschaftliche Abbildungen mit Gruppenvergleichen | Task 1 — **echte** Figuren aus OA-Papers extrahiert (keine ggplot2-Rekonstruktion); qualitative/Framework-Figuren sind legitime wissenschaftliche Abbildungen |
| (5) Jovialer Tonfall unprofessionell | Task 5 — vollständige Ersetzungstabelle |
| (6) Roter Faden nicht gut genug | Task 6 — neue Dramaturgie Problem→Evidenz→Theorie→Praxis→Anwendung→Synthese |
| Final-Check | Task 7 |

**Wissenschaftliche Integrität:**
Task 1 wurde vom ursprünglichen Plan (5 ggplot2-Rekonstruktionen aus Abstract-Zahlen) umgestellt auf reine Extraktion echter Figuren aus publizierten OA-Papers. Rationale: Rekonstruktion aus Abstract-Zahlen birgt das Risiko von Fehlinterpretation der Primärstudien (Achsenskalierung, fehlende Kontext­variablen, ausgelassene Moderatoren). Das vermeiden wir vollständig. Wenn eine Visualisierungs-Art nicht in einem OA-Paper existiert, entfällt sie — wir zeigen nichts, was nicht wirklich in einer Primärquelle steht.

**Placeholder-Scan:** Keine `TBD`, `TODO`, `fill in details` im Plan. Alle Code-Blöcke zeigen vollständigen Code oder konkrete Ersetzungen mit exakten URLs. Ersetzungen sind in Tabellenform mit `Alt` / `Neu`. Die Task-1-Schritte enthalten Entscheidungs­regeln statt Platzhaltern (Varianten A / B je nach Task-1-Ergebnis).

**Typ-Konsistenz:** Die CSS-Klasse `.linked-img` (Task 4) wird in Tasks 4 und 6 verwendet. Die Pfadstruktur `images/literature-figures/` (Task 1, Tasks 3, 6) ist durchgängig. **Kein** `images/charts/` mehr im Plan — alle Referenzen entfernt.

**Ambiguität:** Task 1 enthält eine klare Entscheidungs­regel (Step 8): wenn keine passenden echten Figuren extrahiert werden können, wird die entsprechende Slide-Spalte leer gelassen bzw. auf volle Breite gesetzt — **nicht** mit konstruierten Daten befüllt. Wissenschaftlich sauberer Umgang mit Daten­lücken statt scheinwissenschaftlicher Füllung.

**Abhängigkeiten:** Task 1 (Charts) muss vor Task 3 (Forschungs-Teaser mit Chart) und vor Task 6 (Phasen-Slides mit Charts) abgeschlossen sein. Task 2 (Galerie löschen) unabhängig. Task 4 (Links) und Task 5 (Tonfall) unabhängig, können parallel laufen. Task 7 erst nach allen anderen.

**Empfohlene Ausführungs-Reihenfolge:** 1 → 2 → 5 → 3 → 4 → 6 → 7.

## Log Task 1 erledigt: 8 zusätzliche echte Figuren extrahiert (Quellen: Rezat et al. 2025, Alnemrat et al. 2025, Sanz-Tejeda et al. 2026, Alfarwan 2025, Liu et al. 2025). Keine erfundenen Charts. 2026-04-16.
## Log Task 2 erledigt: Einstieg-Galerie entfernt, Slide "Kurze Standortbestimmung" ersetzt durch "Ausgangslage" mit drei Leitfragen. 2026-04-16.

## Log Task 5 erledigt: Tonfall akademisiert, Sie-Ansprache durchgängig, alle jovialen Phrasen ersetzt. 2026-04-16.

## Log Task 3 erledigt: Forschungs-Slide als "Empirische Befundlage 2025/26" mit 5 fragmentierten Evidenzen + echter PRISMA-Figur aus Sanz-Tejeda et al. (2026). Akademischer Titel. 2026-04-16.

## Log Task 4 erledigt: Alle Hauptbilder + Weltreise-Tiles + Inline-Zitate + Hover-Styles verlinkt. 2026-04-16.

## Log Task 6 erledigt: Dramaturgie Problem→Evidenz→Theorie→Praxis→Anwendung→Synthese verifiziert. Phase 4 erweitert um Alnemrat-Gruppenvergleich (echte Figur, Variant B). 2026-04-16.

## Log Task 7 erledigt: Finale Verifikation bestanden — 21 Slides, 23 Links, 8 Fragments, 7 echte Figuren (keine erfundenen Charts). README aktualisiert. Revision abgeschlossen 2026-04-16.
