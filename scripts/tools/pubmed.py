"""PubMed E-utilities — biomedizinische Publikationen."""
from __future__ import annotations
import httpx

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

async def search_pubmed(query: str, max_results: int = 8) -> list[dict]:
    async with httpx.AsyncClient(timeout=15) as client:
        s = await client.get(f"{BASE}/esearch.fcgi", params={
            "db": "pubmed", "term": query, "retmode": "json", "retmax": max_results, "sort": "relevance",
        })
        s.raise_for_status()
        ids = s.json().get("esearchresult", {}).get("idlist", [])
        if not ids:
            return []
        sum_r = await client.get(f"{BASE}/esummary.fcgi", params={
            "db": "pubmed", "id": ",".join(ids), "retmode": "json",
        })
        sum_r.raise_for_status()
        result = sum_r.json().get("result", {})
    out = []
    for pid in ids:
        doc = result.get(pid, {})
        out.append({
            "pmid": pid,
            "title": doc.get("title"),
            "authors": [a.get("name") for a in doc.get("authors", [])[:5]],
            "journal": doc.get("fulljournalname"),
            "year": (doc.get("pubdate") or "")[:4],
            "doi": next((x["value"] for x in doc.get("articleids", []) if x.get("idtype") == "doi"), None),
        })
    return out
