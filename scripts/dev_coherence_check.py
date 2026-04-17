"""Post-Hoc Coherence Check.

Durchsucht alle Markdown-Artefakte in _output/agent/artifacts/ und meldet
Inkonsistenzen gegen das Fiktiv-Universum (falsche Namen, falsche Jahre etc.).

Aufruf nach einem Dry-Run (aus dem Projektroot):
    python -m scripts.dev_coherence_check
"""
from __future__ import annotations
import sys
from pathlib import Path

# Sicherstellen, dass direktes Aufrufen ("python scripts/dev_coherence_check.py") auch geht
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import config
from scripts.coherence import load_universe, validate_artifact_text


def main() -> int:
    universe_path = config.OUTPUT_DIR / "universe.json"
    if not universe_path.exists():
        print(f"⚠  Kein Universe gefunden unter {universe_path}")
        print("    Bitte zuerst einen Dry-Run durchführen.")
        return 1

    u = load_universe(universe_path)
    total_issues: list[str] = []
    n_files = 0

    for f in sorted(config.ARTIFACTS_DIR.rglob("*.md")):
        text = f.read_text(encoding="utf-8")
        issues = validate_artifact_text(f.name, text, u)
        total_issues.extend(issues)
        n_files += 1

    print(f"Geprüft: {n_files} Markdown-Artefakte")
    if total_issues:
        print(f"⚠  {len(total_issues)} Koherenz-Probleme gefunden:")
        for i in total_issues:
            print(f"   • {i}")
        return 2

    print("✅ Keine Koherenz-Probleme gefunden")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
