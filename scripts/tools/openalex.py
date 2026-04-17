"""OpenAlex-Client für wissenschaftliche Publikationen."""
from __future__ import annotations
import httpx
from typing import Any

BASE = "https://api.openalex.org"

async def search_works(query: str, year_from: int = 2018, per_page: int = 10) -> list[dict[str, Any]]:
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(
            f"{BASE}/works",
            params={
                "search": query,
                "filter": f"from_publication_date:{year_from}-01-01,has_abstract:true,language:de|en",
                "per-page": per_page,
                "mailto": "picts-demo@example.ch",  # OpenAlex empfiehlt
            },
        )
        r.raise_for_status()
        data = r.json()
    results = []
    for w in data.get("results", []):
        results.append({
            "title": w.get("title") or "",
            "authors": [a["author"]["display_name"] for a in w.get("authorships", [])[:5] if a.get("author")],
            "year": w.get("publication_year"),
            "doi": w.get("doi"),
            "venue": (w.get("primary_location") or {}).get("source", {}).get("display_name") if w.get("primary_location") else None,
            "abstract": _reconstruct_abstract(w.get("abstract_inverted_index")),
            "open_access_url": (w.get("open_access") or {}).get("oa_url"),
        })
    return results

def _reconstruct_abstract(inverted_index: dict | None) -> str:
    if not inverted_index:
        return ""
    pos_to_word: dict[int, str] = {}
    for word, positions in inverted_index.items():
        for p in positions:
            pos_to_word[p] = word
    return " ".join(pos_to_word[i] for i in sorted(pos_to_word))
