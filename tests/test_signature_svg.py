from scripts.media.signature_svg import signature_svg

def test_deterministic_same_name():
    a = signature_svg("Luca Brunner")
    b = signature_svg("Luca Brunner")
    assert a == b

def test_different_for_different_name():
    a = signature_svg("Luca Brunner")
    b = signature_svg("Dr. Andrea Weber")
    assert a != b
