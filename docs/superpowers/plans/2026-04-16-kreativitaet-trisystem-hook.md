# Kreativitäts-Paid-Off und Tri-System-Problem-Aufhänger

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Die Animation aus Slide 2 wird als Beleg für KI-Kreativität gesetzt (mit Doshi & Hauser 2024 als Quelle). Gleichzeitig wird die Tri-System-Theorie (Shaw & Nave 2026) zum strukturellen Aufhänger für die Probleme von KI im Bildungskontext.

**Architecture:** Zwei neue Slides direkt nach der Kunstwerk-Animation — eine "War das kreativ?" (Paid-off für Animation, Doshi & Hauser als Beleg), eine "Drei Systeme, drei Risiken" (Tri-System-Problem-Rahmen, Shaw & Nave als Beleg). Beide Slides bereiten den Rest der Präsentation dramaturgisch vor: die Animation wird zu Evidenz, die Warnung wird zu Struktur.

**Tech Stack:** Quarto + revealjs, bestehende zag-theme.scss (keine Änderungen nötig), reine Markdown-HTML-Ergänzungen.

---

## Datei-Inventar

**Zu modifizieren:**
- `slides.qmd` — zwei neue Slides nach Zeile 107 (nach Animation-Slide) einfügen, bestehende Slides rücken
- `docs/literature/2025-2026-KI-Schreibunterricht.md` — Doshi & Hauser (2024) und Shaw & Nave (2026) ergänzen

**Keine neuen Dateien** — beide Slides sind reiner HTML-Content.

**Verifikation:**
- Bildschirm-Screenshots der beiden neuen Slides
- Render muss ohne fenced-div-Warnungen durchlaufen

---

## Task 1: Slide "War das kreativ?" direkt nach Animation

**Files:**
- Modify: `slides.qmd` — neue H2-Slide direkt nach der Kunstwerk-Animation, vor `## Ausgangslage`

**Rationale:** Der User wünscht die Animation als Gegenargument zur These "KI ist nicht kreativ". Die Slide rahmt das Erlebte: Claude hat die Animation (Konzept, Wortauswahl, Choreografie, CSS) selbst entworfen. Als Beleg dient Doshi & Hauser (2024) *Science Advances*: KI-Zugang erhöht individuelle Kreativitäts-Bewertungen signifikant — aber mit Vorsicht bei kollektiver Diversität.

- [ ] **Step 1: Position im File lokalisieren**

```bash
cd /Users/ramonfuglister/Desktop/Coding/picts_input
grep -n "^## Ausgangslage\|^## {.artwork-slide" slides.qmd
```

Erwartung: Zwei Zeilen — die Artwork-Slide-Kopfzeile und die "## Ausgangslage"-Kopfzeile. Die neue Slide wird direkt vor "## Ausgangslage" eingefügt.

- [ ] **Step 2: Neue Slide einfügen**

Verwende Edit-Tool. Ersetze die Zeile `## Ausgangslage` durch den folgenden Block, der die neue Slide **davor** einfügt und dann die bestehende Ausgangslage-Slide unverändert behält:

```markdown
## Die Kunst, die Sie gerade gesehen haben —

<div style="display: grid; grid-template-columns: 1.15fr 1fr; gap: 1.5rem; margin-top: 0.4em; align-items: center;">

<div>

<p style="font-size: 1.1em; line-height: 1.55; margin-bottom: 0.9em;">
<em>Konzept · Wortauswahl · Timing · Farbcode · CSS-Code — alles von Claude entworfen. Keine Vorlage, keine Cliparts.</em>
</p>

<p style="font-size: 0.95em; line-height: 1.55;">
Was bedeutet das für die Diskussion "KI ist (nicht) kreativ"?
</p>

<div class="evidence fragment" data-fragment-index="1" style="margin-top: 1em;">
<div class="evidence-label">Experimentell · N = 293 Schreibende</div>
<div class="evidence-text">KI-generierte Ideen lassen Kurzgeschichten signifikant <strong>kreativer, besser geschrieben und unterhaltsamer</strong> wirken — besonders bei weniger kreativen Schreibenden.</div>
<div class="evidence-source"><a href="https://www.science.org/doi/10.1126/sciadv.adn5290" target="_blank">Doshi &amp; Hauser (2024)</a>, <em>Science Advances, 10</em>(28), Artikel eadn5290.</div>
</div>

<div class="evidence fragment" data-fragment-index="2" style="margin-top: 0.7em; border-left-color: #ff1744;">
<div class="evidence-label" style="color:#ff1744;">Aber — der Preis</div>
<div class="evidence-text">Texte <strong>mit</strong> KI-Input werden <strong>untereinander ähnlicher</strong>. Individuelle Kreativität steigt — kollektive Neuheit sinkt.</div>
<div class="evidence-source">Doshi &amp; Hauser (2024) — "an increase in individual creativity at the risk of losing collective novelty".</div>
</div>

</div>

<div class="fragment" data-fragment-index="3" style="text-align: center; padding: 1.5rem 1rem; background: #f4f4f2; border-radius: 12px;">
<div style="font-size: 1.3em; line-height: 1.4; color: #e30059; font-weight: 600;">
"Individuell kreativer.<br>Kollektiv einförmiger."
</div>
<div style="margin-top: 0.8em; font-size: 0.75em; color: #666; font-style: italic;">
Der produktive und der problematische Effekt in einem Satz.
</div>
</div>

</div>
```

Anschliessend die Zeile `## Ausgangslage` unverändert unterhalb belassen.

Exakter Edit-Befehl (alter String → neuer String): Suche `## Ausgangslage` (erstes Vorkommen nach der Animation) und ersetze durch den obigen Block + Leerzeile + `## Ausgangslage`.

- [ ] **Step 3: Literatur-File ergänzen**

Edit `docs/literature/2025-2026-KI-Schreibunterricht.md`. In der Sektion "International peer-reviewed" → "Empirisch" die folgende Referenz einfügen (alphabetisch nach Autor):

```markdown
✅ Doshi, A. R., & Hauser, O. P. (2024). Generative AI enhances individual creativity but reduces the collective diversity of novel content. *Science Advances, 10*(28), Artikel eadn5290. https://doi.org/10.1126/sciadv.adn5290
  → Online-Experiment mit 293 Schreibenden + 600 Evaluierenden: KI-Ideen steigern individuelle Kreativitäts-Bewertungen, aber Texte werden homogener.
```

- [ ] **Step 4: Render**

```bash
cd /Users/ramonfuglister/Desktop/Coding/picts_input
export PATH="$HOME/tools/bin:$PATH"
quarto render slides.qmd --to revealjs 2>&1 | tail -3
```

Erwartung: `Output created: _output/slides.html`, keine fenced-div-Warnungen.

- [ ] **Step 5: Visuelle Verifikation**

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p _check/new2
"$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars --screenshot="_check/new2/kreativitaet.png" --window-size=1280,720 --virtual-time-budget=4000 "file://$(pwd)/_output/slides.html#/1" 2>/dev/null
```

Note: Slide-Index kann abweichen. Probiere `#/1`, `#/2`, `#/3`. Die neue Slide "Die Kunst, die Sie gerade gesehen haben —" sollte zwischen Titel/Animation und Ausgangslage liegen.

Lies die PNG mit Read-Tool. Erwartung: akademischer Titel oben, zwei Evidenz-Kästen links, Hero-Zitat rechts ("Individuell kreativer. Kollektiv einförmiger.").

---

## Task 2: Slide "Drei Systeme, drei Risiken" nach "Kreativ?" und vor "Ausgangslage"

**Files:**
- Modify: `slides.qmd` — neue H2-Slide direkt nach der Task-1-Slide, vor `## Ausgangslage`

**Rationale:** User-Wunsch: "ich will das mit den 3 system aus dem paper als aufhänger für die probleme von KI". Die Tri-System-Theorie (Shaw & Nave 2026) dient als strukturelles Raster für die drei zentralen KI-Risiken im Bildungskontext.

- [ ] **Step 1: Neuen Block direkt vor `## Ausgangslage` einfügen**

Zwischen der Task-1-Slide und der bestehenden Ausgangslage-Slide diesen neuen Block einfügen:

```markdown
## Drei Systeme, drei Risiken

<div style="font-size: 0.95em; margin-top: 0.3em; color: #666;">
Die Kehrseite der Kreativitätssteigerung — geordnet nach der Tri-System-Theorie (<a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6097646" target="_blank">Shaw &amp; Nave, 2026</a>).
</div>

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1.2em;">

<div class="evidence" style="border-left-color: #7a00df; margin: 0;">
<div class="evidence-label" style="color: #7a00df;">System 1 · intuitiv</div>
<div class="evidence-text" style="font-size: 0.9em; line-height: 1.5;">
<strong>Was ausfällt:</strong> Die Intuition "hier stimmt etwas nicht" wird betäubt, wenn KI-Text flüssig klingt.
</div>
<div class="evidence-source" style="font-size: 0.72em; margin-top: 0.6em;">
Folge: Fehler in KI-Ausgaben bleiben unbemerkt.
</div>
</div>

<div class="evidence" style="border-left-color: #7a00df; margin: 0;">
<div class="evidence-label" style="color: #7a00df;">System 2 · deliberativ</div>
<div class="evidence-text" style="font-size: 0.9em; line-height: 1.5;">
<strong>Was umgangen wird:</strong> Das mühsame Durchdenken entfällt, wenn die Antwort sofort vorliegt.
</div>
<div class="evidence-source" style="font-size: 0.72em; margin-top: 0.6em;">
Folge: Lernen durch Anstrengung findet nicht statt.
</div>
</div>

<div class="evidence" style="border-left-color: #ff1744; margin: 0;">
<div class="evidence-label" style="color: #ff1744;">System 3 · artifiziell</div>
<div class="evidence-text" style="font-size: 0.9em; line-height: 1.5;">
<strong>Was aussen bleibt:</strong> Die Kognition liegt ausserhalb des Gehirns — System 3 denkt für den Menschen mit.
</div>
<div class="evidence-source" style="font-size: 0.72em; margin-top: 0.6em;">
Folge: Kein Gedächtnis, keine Transferleistung.
</div>
</div>

</div>

<div class="evidence fragment" data-fragment-index="1" style="border-left-color: #ff1744; margin-top: 1.2em;">
<div class="evidence-label" style="color: #ff1744;">Empirische Konsequenz · Cognitive Surrender</div>
<div class="evidence-text">Akkuratheit steigt um <strong>+25 pp</strong> bei korrekter KI, fällt um <strong>−15 pp</strong> bei fehlerhafter — besonders bei Personen mit tiefem <em>need for cognition</em>.</div>
<div class="evidence-source"><a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6097646" target="_blank">Shaw &amp; Nave (2026)</a>, SSRN 6097646 · N = 1 372 · 9 593 Trials.</div>
</div>
```

- [ ] **Step 2: Forschungs-Slide entstauben**

Da Shaw & Nave nun auf der Problem-Aufhänger-Slide zentral sind, entferne die 6. Evidenz (Shaw & Nave) aus der "Empirische Befundlage"-Slide, um Doppelung zu vermeiden.

Suche in `slides.qmd`:

```html
<div class="evidence fragment" data-fragment-index="6" style="border-left-color: #ff1744;">
<div class="evidence-label" style="color:#ff1744;">Tri-System-Theorie · Kognitive Kapitulation</div>
<div class="evidence-text">N = 1 372 · 9 593 Trials: Akkuratheit steigt +25 pp bei korrekter KI, fällt −15 pp bei fehlerhafter — am stärksten bei tiefem <em>need for cognition</em>.</div>
<div class="evidence-source"><a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6097646" target="_blank">Shaw &amp; Nave (2026)</a>, SSRN 6097646 · Wharton Research Paper.</div>
</div>
```

und **entferne diesen Block vollständig** (inklusive vorausgehender Leerzeile). Der Index-7 im folgenden `<div class="fragment" data-fragment-index="7">` bleibt unverändert — Revealjs akzeptiert nicht-lückenlose Indizes.

- [ ] **Step 3: Literatur ergänzen**

Shaw & Nave ist bereits aus dem früheren Commit in der Literatur enthalten? Prüfen:

```bash
grep -n "Shaw.*Nave\|6097646" /Users/ramonfuglister/Desktop/Coding/picts_input/docs/literature/2025-2026-KI-Schreibunterricht.md
```

Falls nicht gefunden: In Sektion "International peer-reviewed · Theoretisch / Konzeptuell" ergänzen:

```markdown
✅ Shaw, S. D., & Nave, G. (2026). Thinking—Fast, Slow, and Artificial: How AI is reshaping human reasoning and the rise of cognitive surrender [Working Paper]. Wharton School, University of Pennsylvania. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6097646
  → Tri-System-Theorie: System 1 (intuition) + System 2 (deliberation) + System 3 (artificial). N = 1 372; +25/−15 pp Akkuratheit bei korrekter/fehlerhafter KI.
```

- [ ] **Step 4: Render + Screenshot**

```bash
cd /Users/ramonfuglister/Desktop/Coding/picts_input
export PATH="$HOME/tools/bin:$PATH"
quarto render slides.qmd --to revealjs 2>&1 | tail -3
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars --screenshot="_check/new2/drei-risiken.png" --window-size=1280,720 --virtual-time-budget=4000 "file://$(pwd)/_output/slides.html#/2" 2>/dev/null
```

Read-Tool auf `_check/new2/drei-risiken.png`. Erwartung: Drei-Spalten-Raster (System 1 lila · System 2 lila · System 3 rot), darunter rote Cognitive-Surrender-Evidenz.

---

## Task 3: Titel-Texte der 4 Phasen-Slides im Browser verifizieren

**Files:** keine Änderungen, nur Verifikation

**Rationale:** User meldete "wie echte Lehrpersonen" — das ist bereits behoben (grep = 0), aber der User sieht vermutlich den alten Render.

- [ ] **Step 1: Bestätigen, dass alle vier Phasen-Titel neu sind**

```bash
cd /Users/ramonfuglister/Desktop/Coding/picts_input
grep -n "^## Phase" slides.qmd
```

Erwartung:
```
## Phase 1: Planen · Blume · Mollick · Kentz
## Phase 1: Empirische Befunde zur realen KI-Nutzung
## Phase 2: Strukturieren · UNC · Oxford · PHZH iArgue
## Phase 2: Forschungsprojekt iArgue (PHZH)
## Phase 3: Formulieren · Wampfler · LSE · Roberts
## Phase 3: PCRR-Framework (PH Tirol)
## Phase 4: Überarbeiten · Haverkamp · Mollick · Kentz
## Phase 4: Adaptives KI-Feedback — ArguaTutor
```

Falls eine noch `wie echte Lehrpersonen` enthält → mit Edit-Tool fixen nach gleichem Muster (`Phase N: Thema · Autor · Autor · Autor`).

---

## Task 4: Cheat-Sheet- und Schülertext-Handouts neu rendern

**Files:**
- Modify: `_output/handout/cheatsheet.pdf`, `_output/handout/schuelertext-mira-imhof.pdf` (automatisch durch render)

- [ ] **Step 1: Handouts re-rendern und PDF erneut drucken**

```bash
cd /Users/ramonfuglister/Desktop/Coding/picts_input
export PATH="$HOME/tools/bin:$PATH"
cd handout && quarto render cheatsheet.qmd 2>&1 | tail -1
quarto render schuelertext-mira-imhof.qmd 2>&1 | tail -1
cd ..
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless --disable-gpu --no-sandbox --no-pdf-header-footer --print-to-pdf="_output/handout/cheatsheet.pdf" "file://$(pwd)/_output/handout/cheatsheet.html" 2>/dev/null
"$CHROME" --headless --disable-gpu --no-sandbox --no-pdf-header-footer --print-to-pdf="_output/handout/schuelertext-mira-imhof.pdf" "file://$(pwd)/_output/handout/schuelertext-mira-imhof.html" 2>/dev/null
ls -la _output/handout/
```

Erwartung: beide PDFs aktualisiert (neuer Zeitstempel).

---

## Task 5: Commit + Push

**Files:** git repository

- [ ] **Step 1: Staging**

```bash
cd /Users/ramonfuglister/Desktop/Coding/picts_input
git add -A
git status | head -15
```

- [ ] **Step 2: Commit**

```bash
git commit -m "$(cat <<'EOF'
Kreativitäts-Paid-Off + Tri-System als Problem-Aufhänger

Zwei neue Slides direkt nach der Kunstwerk-Animation:

1. "Die Kunst, die Sie gerade gesehen haben —"
   Rahmt die Animation als Beleg für KI-Kreativität.
   Paid-off durch Doshi & Hauser (2024), Science Advances: N=293,
   KI-Ideen steigern individuelle Kreativitäts-Bewertungen
   signifikant, aber Texte werden kollektiv ähnlicher.
   Hero-Frame: "Individuell kreativer. Kollektiv einförmiger."

2. "Drei Systeme, drei Risiken"
   Tri-System-Theorie (Shaw & Nave 2026) als strukturelles Raster
   für die drei zentralen KI-Risiken: System 1 (Intuition betäubt),
   System 2 (Deliberation umgangen), System 3 (Kognition aussen).
   Cognitive Surrender als empirische Konsequenz (+25/-15 pp).

Shaw & Nave aus Empirische-Befundlage-Slide entfernt (Doppelung
vermieden; bleibt dort über die Animation präsent).

Literaturverzeichnis ergänzt um Doshi & Hauser (2024) und
formal ergänzt um Shaw & Nave (2026).

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)" 2>&1 | tail -5
```

- [ ] **Step 3: Push**

```bash
git push origin main 2>&1 | tail -3
```

Erwartung: `main -> main` erfolgreich gepusht.

---

## Self-Review

**Spec-Abdeckung:**

| User-Wunsch | Task |
|---|---|
| "Animation als Beispiel für Kreativität (Gegenargument)" | Task 1 — Slide mit Doshi & Hauser als Beleg |
| "Gerne auch mit Paper" | Task 1 — Doshi & Hauser (2024) Science Advances verlinkt |
| "3 System aus dem Paper als Aufhänger für Probleme" | Task 2 — Slide "Drei Systeme, drei Risiken" mit Shaw & Nave |
| Titel "wie echte Lehrpersonen" | Task 3 — Verifikation (bereits behoben) |
| Handouts aktuell halten | Task 4 |
| Auf GitHub pushen | Task 5 |

**Placeholder-Scan:** Keine TBD, alle Ersetzungen als vollständiger HTML-Block in Edit-Position spezifiziert.

**Typ-Konsistenz:** CSS-Klassen `.evidence`, `.evidence-label`, `.evidence-text`, `.evidence-source`, `.fragment` sind bereits im Theme definiert. Keine neuen Klassen.

**Reihenfolge der Slides nach Ausführung:**
1. Titel
2. Kunstwerk-Animation
3. **Die Kunst, die Sie gerade gesehen haben —** (NEU)
4. **Drei Systeme, drei Risiken** (NEU)
5. Ausgangslage
6. Empirische Befundlage (Shaw & Nave hier entfernt)
7. Theoretischer Rahmen
8. … (wie bisher)

Diese Sequenz erzeugt dramaturgisch: WOW → Credit → Warning → 3 Leitfragen → Evidenz → Theorie → Praxis — doppelter Hook (Anerkennung + Gefahr) ist stärker als einfacher Wow-Moment.
