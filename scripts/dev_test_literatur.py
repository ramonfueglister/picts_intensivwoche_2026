import asyncio
from scripts.coherence import Universe
from scripts.subagents import literatur

async def main():
    u = Universe.sample()
    result, quellen = await literatur.run(u)
    print(f"✅ {len(quellen)} Quellen in {result.duration_s:.1f}s")
    for q in quellen:
        print(f"  [{q.typ}] {q.autor} — {q.titel} ({q.jahr})")

asyncio.run(main())
