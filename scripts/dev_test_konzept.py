"""Einmaliger Test: Konzept-Agent alleine ausführen."""
import asyncio
from scripts.coherence import Universe
from scripts.subagents import konzept

async def main():
    u = Universe.sample()
    result = await konzept.run(u)
    print(f"✅ {result.output_path} in {result.duration_s:.1f}s")

if __name__ == "__main__":
    asyncio.run(main())
