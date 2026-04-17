# tests/test_pdf_render.py
import pytest
from pathlib import Path
from scripts.media.pdf_render import render_markdown_to_pdf

def test_render_simple(tmp_path):
    md = "# Test\n\nEin kleiner Absatz."
    out = tmp_path / "out.pdf"
    meta = {"u": None, "title": "Test"}
    render_markdown_to_pdf(md, out, template_name="konzept_html.j2", extra_ctx={"u": _sample_u()})
    assert out.exists()
    assert out.stat().st_size > 1000  # mind. 1 KB

def _sample_u():
    from scripts.coherence import Universe
    return Universe.sample()
