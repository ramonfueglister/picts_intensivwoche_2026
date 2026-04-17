"""Google Books API — echte Bücher mit ISBN & Snippets."""
from __future__ import annotations
import httpx

BASE = "https://www.googleapis.com/books/v1/volumes"

async def search_books(query: str, max_results: int = 8, lang: str = "de") -> list[dict]:
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(BASE, params={
            "q": query,
            "maxResults": max_results,
            "langRestrict": lang,
            "printType": "books",
        })
        r.raise_for_status()
        data = r.json()
    out = []
    for item in data.get("items", []):
        info = item.get("volumeInfo", {})
        ids = {x["type"]: x["identifier"] for x in info.get("industryIdentifiers", [])}
        out.append({
            "title": info.get("title"),
            "authors": info.get("authors", []),
            "publisher": info.get("publisher"),
            "year": (info.get("publishedDate") or "")[:4],
            "isbn_13": ids.get("ISBN_13"),
            "isbn_10": ids.get("ISBN_10"),
            "description": info.get("description"),
            "preview_link": info.get("previewLink"),
            "info_link": info.get("infoLink"),
            "snippet": (item.get("searchInfo") or {}).get("textSnippet"),
        })
    return out
