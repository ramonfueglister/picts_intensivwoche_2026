from fastapi.testclient import TestClient
from scripts.server import app

def test_root_returns_html():
    client = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200
    assert "VA-Agent" in r.text

def test_status_initial():
    client = TestClient(app)
    r = client.get("/api/status")
    assert r.status_code == 200
    assert "state" in r.json()
