from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_readiness():
    assert client.get("/ready").json()["status"] == "ready"


def test_root_contract():
    body = client.get("/").json()
    assert body["service"] == "resilience-api"
    assert body["status"] == "ok"


def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text
