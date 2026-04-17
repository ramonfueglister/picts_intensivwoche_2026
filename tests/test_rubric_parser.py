from scripts.rubric_parser import load_rubric, Rubric

def test_rubric_has_120_points():
    r = load_rubric()
    total = r.teile["A_prozess"].max + r.teile["B_produkt"].max + r.teile["C_praesentation"].max
    assert total == 120

def test_konzeptbeschrieb_has_9_points():
    r = load_rubric()
    kriterien = {k.name: k for k in r.teile["A_prozess"].kriterien}
    assert kriterien["Konzeptbeschrieb"].max == 9

def test_notenskala_5_at_90():
    r = load_rubric()
    # Suche: bei 90 Punkten muss Note 5.0 sein
    for punkte, note in r.notenskala:
        if punkte == 90:
            assert note == 5.0
            return
    raise AssertionError("Keine Eintrag 90 Punkte in Notenskala")
