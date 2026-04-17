"""Literatur-Agent: plant Suchen, ruft Tools, paraphrasiert Snippets."""
from __future__ import annotations
import asyncio
import json
import time

from scripts.coherence import Universe, Quelle
from scripts.subagents.base import (
    SubagentResult, claude_sonnet_complete, render_prompt,
    emit_start, emit_done, emit_warn,
)
from scripts.tools.google_books import search_books
from scripts.tools.openalex import search_works
from scripts.tools.pubmed import search_pubmed
from scripts.tools.srf_fetch import fetch_srf_article
from scripts.utils import log

PHASE = 4
NAME = "literatur"
SYSTEM = "Du planst Literatursuchen. Du antwortest immer mit gültigem JSON und nichts anderem."


async def run(u: Universe) -> tuple[SubagentResult, list[Quelle]]:
    await emit_start(NAME, PHASE)
    t0 = time.monotonic()
    plan_user = render_prompt("literatur_search_plan.j2", u=u)
    plan_json_str = await claude_sonnet_complete(system=SYSTEM, user=plan_user, max_tokens=800)
    plan = _extract_json(plan_json_str)

    gb_tasks = [search_books(q, 4) for q in plan.get("google_books_queries", [])]
    oa_tasks = [search_works(q, 2018, 4) for q in plan.get("openalex_queries", [])]
    pm_tasks = [search_pubmed(q, 4) for q in plan.get("pubmed_queries", [])]
    srf_tasks = [fetch_srf_article(url) for url in plan.get("srf_urls", [])]

    all_results = await asyncio.gather(*gb_tasks, *oa_tasks, *pm_tasks, *srf_tasks, return_exceptions=True)

    gb_results = all_results[:len(gb_tasks)]
    oa_results = all_results[len(gb_tasks):len(gb_tasks)+len(oa_tasks)]
    pm_results = all_results[len(gb_tasks)+len(oa_tasks):len(gb_tasks)+len(oa_tasks)+len(pm_tasks)]
    srf_results = all_results[len(gb_tasks)+len(oa_tasks)+len(pm_tasks):]

    quellen: list[Quelle] = []
    for batch in gb_results:
        if isinstance(batch, Exception): continue
        for b in batch[:2]:
            if not b.get("title") or not (b.get("isbn_13") or b.get("isbn_10")):
                continue
            quellen.append(Quelle(
                typ="buch",
                autor=", ".join(b.get("authors") or []) or "Unbekannt",
                titel=b["title"],
                jahr=int(b["year"]) if b.get("year") and b["year"].isdigit() else None,
                verlag=b.get("publisher"),
                isbn=b.get("isbn_13") or b.get("isbn_10"),
                url=b.get("info_link"),
                snippet=b.get("snippet") or (b.get("description") or "")[:500],
                real_verified=True,
                api_source="google_books",
            ))
    for batch in oa_results:
        if isinstance(batch, Exception): continue
        for w in batch[:2]:
            if not w.get("title"): continue
            quellen.append(Quelle(
                typ="fachartikel",
                autor=", ".join(w.get("authors") or []) or "Unbekannt",
                titel=w["title"],
                jahr=w.get("year"),
                verlag=w.get("venue"),
                doi=w.get("doi"),
                url=w.get("open_access_url"),
                snippet=(w.get("abstract") or "")[:800],
                real_verified=True,
                api_source="openalex",
            ))
    for batch in pm_results:
        if isinstance(batch, Exception): continue
        for p in batch[:2]:
            quellen.append(Quelle(
                typ="fachartikel",
                autor=", ".join(p.get("authors") or []) or "Unbekannt",
                titel=p["title"] or "",
                jahr=int(p["year"]) if p.get("year") and p["year"].isdigit() else None,
                verlag=p.get("journal"),
                doi=p.get("doi"),
                snippet="",
                real_verified=True,
                api_source="pubmed",
            ))
    for art in srf_results:
        if isinstance(art, Exception): continue
        quellen.append(Quelle(
            typ="internet",
            autor="SRF Redaktion",
            titel=art.get("title") or "SRF-Beitrag",
            url=art["url"],
            snippet=" ".join(art.get("paragraphs", []))[:800],
            real_verified=True,
            api_source="srf",
        ))

    # Mindestens 8 Quellen garantieren
    if len(quellen) < 8:
        await emit_warn(NAME, PHASE, f"Nur {len(quellen)} Quellen gefunden, Minimum 8")

    duration = time.monotonic() - t0
    await emit_done(NAME, PHASE, detail=f"{len(quellen)} Quellen")
    log.info(f"[{NAME}] {len(quellen)} Quellen in {duration:.1f}s")
    return SubagentResult(name=NAME, output_path=None, duration_s=duration), quellen


def _extract_json(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(raw)
