import os

from fastapi.testclient import TestClient

os.environ.setdefault("DJANGO_SECRET_KEY", "test-secret-key")

from app.main import app


client = TestClient(app)


def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_legacy_route_is_mounted():
    response = client.get("/research/")
    assert response.status_code == 200
