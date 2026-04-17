"""Runtime-Settings, aus .env geladen via python-dotenv."""
from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)  # .env gewinnt über Shell-Env (falls Shell leere Shadow-Variablen hat)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "_output" / "agent"
ARTIFACTS_DIR = OUTPUT_DIR / "artifacts"
PRERENDERED_DIR = OUTPUT_DIR / "prerendered"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
PROMPTS_DIR = PROJECT_ROOT / "scripts" / "prompts"
WEGLEITUNG_PDF = Path.home() / "Desktop" / "ABU_VA_Wegleitung_FaGe_Version12_2025.pdf"

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID_LUCA = os.getenv("ELEVENLABS_VOICE_ID_LUCA", "")
ELEVENLABS_VOICE_ID_DRWEBER = os.getenv("ELEVENLABS_VOICE_ID_DRWEBER", "elsa")
RUNWAYML_API_KEY = os.getenv("RUNWAYML_API_KEY")
HEDRA_API_KEY = os.getenv("HEDRA_API_KEY")
FAL_KEY = os.getenv("FAL_KEY")
VA_AGENT_PORT = int(os.getenv("VA_AGENT_PORT", "8001"))
USE_PRERENDERED = os.getenv("USE_PRERENDERED", "0") == "1"
VA_AGENT_TOPIC = os.getenv("VA_AGENT_TOPIC", "Einsamkeit im Alter")
VA_AGENT_RAHMEN = os.getenv("VA_AGENT_RAHMEN", "Gegensätze")

CLAUDE_MODEL_OPUS = "claude-opus-4-6"
CLAUDE_MODEL_SONNET = "claude-sonnet-4-6"

def ensure_dirs():
    for d in (OUTPUT_DIR, ARTIFACTS_DIR, PRERENDERED_DIR):
        d.mkdir(parents=True, exist_ok=True)

ensure_dirs()
