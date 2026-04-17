"""Einmaliger Dev-Test: hört die geklonte Stimme einen Testsatz sprechen?"""
from elevenlabs.client import ElevenLabs
from scripts import config
from pathlib import Path

client = ElevenLabs(api_key=config.ELEVENLABS_API_KEY)
audio = client.text_to_speech.convert(
    voice_id=config.ELEVENLABS_VOICE_ID_LUCA,
    model_id="eleven_multilingual_v2",
    text="Grüezi Frau Doktor Weber, mein Name ist Luca Brunner. Ich mache gerade meine Vertiefungsarbeit zum Thema Einsamkeit im Alter.",
    output_format="mp3_44100_128",
)
out = Path("_output/agent/voice_test_luca.mp3")
out.parent.mkdir(parents=True, exist_ok=True)
with out.open("wb") as f:
    for chunk in audio:
        f.write(chunk)
print(f"✅ {out}")
