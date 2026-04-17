from pathlib import Path
from scripts.coherence import Universe, load_universe, save_universe, validate_artifact_text

def test_universe_roundtrip(tmp_path):
    u = Universe.sample()
    p = tmp_path / "u.json"
    save_universe(u, p)
    loaded = load_universe(p)
    assert loaded.schuelerin.vorname == u.schuelerin.vorname
    assert loaded.interviewperson.name_anzeige == u.interviewperson.name_anzeige

def test_validate_artifact_detects_wrong_name():
    u = Universe.sample()
    text = "Das Interview mit Dr. Müller war spannend."
    issues = validate_artifact_text("test.txt", text, u)
    assert any("Dr. Müller" in i or "name" in i.lower() for i in issues)

def test_validate_artifact_accepts_correct():
    u = Universe.sample()
    text = f"Das Interview mit {u.interviewperson.name_anzeige} war spannend."
    issues = validate_artifact_text("test.txt", text, u)
    assert issues == []
