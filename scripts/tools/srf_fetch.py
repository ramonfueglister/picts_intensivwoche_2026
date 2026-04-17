"""SRF-Artikel holen (nur für Whitelist-URLs)."""
from __future__ import annotations
import httpx
from bs4 import BeautifulSoup

ALLOWED_HOSTS = {"www.srf.ch", "srf.ch"}

async def fetch_srf_article(url: str) -> dict:
    from urllib.parse import urlparse
    host = urlparse(url).hostname
    if host not in ALLOWED_HOSTS:
        raise ValueError(f"Host {host} nicht in Whitelist")
    async with httpx.AsyncClient(timeout=15, headers={"User-Agent": "Mozilla/5.0"}) as client:
        r = await client.get(url)
        r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.find("h1").get_text(strip=True) if soup.find("h1") else ""
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")][:8]
    return {"url": url, "title": title, "paragraphs": paragraphs}
