"""Umfrage-Agent: Fragebogen, synthetische Antworten, Plots, Auswertungstext."""
from __future__ import annotations
import io
import json
import time
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from scripts import config
from scripts.coherence import Universe
from scripts.subagents.base import (
    SubagentResult, claude_opus_complete, claude_sonnet_complete, render_prompt,
    emit_start, emit_done, emit_warn,
)
from scripts.media.pdf_render import render_markdown_to_pdf
from scripts.utils import log

PHASE = 4
NAME = "umfrage"
SYSTEM_JSON = "Du antwortest immer mit reinem JSON, keine Markdown-Fences."
SYSTEM_CSV = "Du antwortest immer mit reinem CSV, kein Kommentar davor oder danach."


async def run(u: Universe) -> tuple[SubagentResult, str]:
    """Returns (result, auswertungstext_md)."""
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()

    fragebogen_json = await claude_opus_complete(
        system=SYSTEM_JSON,
        user=render_prompt("umfrage_fragebogen.j2", u=u),
        max_tokens=2048,
    )
    try:
        fragebogen = _extract_json(fragebogen_json)
    except Exception as e:
        await emit_warn(NAME, PHASE, f"JSON-Parse fehlgeschlagen: {e}")
        raise

    # Fragebogen-PDF rendern
    fb_md = _fragebogen_to_markdown(fragebogen, u)
    fb_pdf = config.ARTIFACTS_DIR / "15_umfrage_fragebogen.pdf"
    render_markdown_to_pdf(fb_md, fb_pdf, template_name="konzept_html.j2", extra_ctx={"u": u})

    # Antworten generieren
    answers_csv = await claude_opus_complete(
        system=SYSTEM_CSV,
        user=render_prompt("umfrage_antworten.j2", u=u, fragebogen_json=json.dumps(fragebogen, ensure_ascii=False)),
        max_tokens=8000,
    )
    answers_csv = answers_csv.strip()
    if answers_csv.startswith("```"):
        answers_csv = answers_csv.split("\n", 1)[1].rsplit("```", 1)[0]
    csv_path = config.ARTIFACTS_DIR / "16_umfrage_rohdaten.csv"
    csv_path.write_text(answers_csv, encoding="utf-8")

    df = pd.read_csv(io.StringIO(answers_csv))
    # 5 Plots
    plots_dir = config.ARTIFACTS_DIR / "16_plots"
    plots_dir.mkdir(exist_ok=True)
    _plot_demografie_pie(df, plots_dir / "plot1_alter.png")
    _plot_rolle_bar(df, plots_dir / "plot2_rolle.png")
    _plot_likert(df, plots_dir / "plot3_likert.png", fragebogen)
    _plot_kreuz(df, plots_dir / "plot4_kreuz.png", fragebogen)
    _plot_open_wordlen(df, plots_dir / "plot5_offen.png")

    # Auswertungstext ~800 Wörter
    auswertung_md = await claude_sonnet_complete(
        system="Du schreibst eine Umfrage-Auswertung für eine VA. Im Stil einer engagierten FaGe-Lernenden. Doppelpunkt-Gendern. ICH-Form.",
        user=f"""Schreibe eine Auswertung der Umfrage (ca. 800 Wörter, Markdown ohne H1).

Fragebogen: {json.dumps(fragebogen, ensure_ascii=False)}
Rohdaten-Übersicht:
- N = {len(df)}
- Demografie Alter: {df['alter_gruppe'].value_counts().to_dict()}
- Demografie Rolle: {df['rolle'].value_counts().to_dict()}

Struktur:
## Methode
## Rücklauf (N={len(df)}, Versand N={u.umfrage.n_versendet}, Zeitraum {u.umfrage.zeitraum})
## Ergebnisse (2-3 Kernbefunde mit Zahlen, verweise auf Abbildungen "(siehe Abb. 3)")
## Interpretation und Limitationen
""",
        max_tokens=2500,
    )

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"N={len(df)}, 5 Plots")
    log.info(f"[{NAME}] Umfrage fertig in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=csv_path, duration_s=duration), auswertung_md


def _extract_json(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(raw)


def _fragebogen_to_markdown(fb: dict, u: Universe) -> str:
    lines = [f"# {fb.get('titel', 'Umfrage')}", "", fb.get("einleitung", ""), ""]
    lines.append(f"**URL:** {u.umfrage.url_anzeige}")
    lines.append(f"**Zeitraum:** {u.umfrage.zeitraum}")
    lines.append(f"**Versand:** {u.umfrage.n_versendet} Personen · **Rücklauf:** {u.umfrage.n_ruecklauf}")
    lines.append("")
    for f in fb.get("fragen", []):
        lines.append(f"**Frage {f['nr']}** ({f['typ']}): {f['frage']}")
        for opt in f.get("optionen", []):
            lines.append(f"- ☐ {opt}")
        lines.append("")
    return "\n".join(lines)


def _plot_demografie_pie(df: pd.DataFrame, out: Path):
    fig, ax = plt.subplots(figsize=(6, 5))
    vc = df["alter_gruppe"].value_counts()
    ax.pie(vc.values, labels=vc.index, autopct="%1.0f%%", startangle=90, colors=["#e30059", "#7a00df", "#d95f5f", "#f4c430"])
    ax.set_title("Demografie — Altersverteilung (N=%d)" % len(df))
    fig.tight_layout(); fig.savefig(out, dpi=120); plt.close(fig)


def _plot_rolle_bar(df: pd.DataFrame, out: Path):
    fig, ax = plt.subplots(figsize=(7, 4))
    vc = df["rolle"].value_counts()
    ax.bar(vc.index, vc.values, color="#e30059")
    ax.set_ylabel("Anzahl"); ax.set_title("Rollenverteilung der Teilnehmenden")
    fig.tight_layout(); fig.savefig(out, dpi=120); plt.close(fig)


def _plot_likert(df: pd.DataFrame, out: Path, fb: dict):
    likert_cols = []
    for f in fb.get("fragen", []):
        if f["typ"] == "likert_5" and f"f{f['nr']}" in df.columns:
            likert_cols.append((f"f{f['nr']}", f["frage"][:40] + "…"))
    if not likert_cols:
        fig, ax = plt.subplots(); ax.text(0.5, 0.5, "keine Likert-Fragen", ha="center"); fig.savefig(out); plt.close(fig); return
    fig, ax = plt.subplots(figsize=(8, 4))
    for col, label in likert_cols[:4]:
        try:
            vals = pd.to_numeric(df[col], errors="coerce").dropna()
            counts = [(vals == i).sum() for i in range(1, 6)]
            ax.plot(range(1, 6), counts, marker="o", label=label)
        except Exception:
            continue
    ax.set_xticks(range(1, 6)); ax.set_xlabel("Skala 1-5"); ax.set_ylabel("Anzahl")
    ax.set_title("Likert-Antworten"); ax.legend(fontsize=7, loc="best")
    fig.tight_layout(); fig.savefig(out, dpi=120); plt.close(fig)


def _plot_kreuz(df: pd.DataFrame, out: Path, fb: dict):
    fig, ax = plt.subplots(figsize=(7, 4))
    try:
        ct = pd.crosstab(df["alter_gruppe"], df["rolle"])
        im = ax.imshow(ct.values, aspect="auto", cmap="magma")
        ax.set_xticks(range(len(ct.columns))); ax.set_xticklabels(ct.columns, rotation=20, ha="right")
        ax.set_yticks(range(len(ct.index))); ax.set_yticklabels(ct.index)
        for i in range(len(ct.index)):
            for j in range(len(ct.columns)):
                ax.text(j, i, str(ct.values[i, j]), ha="center", va="center", color="white")
        fig.colorbar(im, ax=ax)
        ax.set_title("Kreuztabelle Alter × Rolle")
    except Exception as e:
        ax.text(0.5, 0.5, f"Fehler: {e}", ha="center")
    fig.tight_layout(); fig.savefig(out, dpi=120); plt.close(fig)


def _plot_open_wordlen(df: pd.DataFrame, out: Path):
    fig, ax = plt.subplots(figsize=(7, 3.5))
    # Finde offene Spalten (objekt-dtype mit Text)
    open_cols = [c for c in df.columns if c.startswith("f") and df[c].dtype == object]
    lengths = []
    for c in open_cols:
        for val in df[c].dropna():
            if isinstance(val, str) and len(val) > 5:
                lengths.append(len(val.split()))
    if lengths:
        ax.hist(lengths, bins=12, color="#7a00df")
        ax.set_xlabel("Wörter pro Antwort"); ax.set_ylabel("Häufigkeit")
        ax.set_title(f"Offene Antworten: Wortlängen (n={len(lengths)})")
    else:
        ax.text(0.5, 0.5, "keine offenen Antworten", ha="center")
    fig.tight_layout(); fig.savefig(out, dpi=120); plt.close(fig)
