from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ecosystem() -> None:
    response = client.get("/ecosystem")
    assert response.status_code == 200
    payload = response.json()
    assert "services" in payload
    services = payload["services"]
    assert len(services) == 9
    ids = {s["id"] for s in services}
    assert "franceconnect" in ids
    assert "save_service" in ids
    assert all(
        {"id", "name", "role", "base_url", "docs_hint"} <= set(s.keys()) for s in services
    )


def test_ecosystem_env_override(monkeypatch) -> None:
    monkeypatch.setenv("SNCF_CONNECT_BASE_URL", "http://custom-sncf:8005")
    response = client.get("/ecosystem")
    assert response.status_code == 200
    sncf = next(s for s in response.json()["services"] if s["id"] == "sncf_connect")
    assert sncf["base_url"] == "http://custom-sncf:8005"


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_services_provider_filter() -> None:
    response = client.get("/services", params={"provider": "cpam"})
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["items"]) == 2
    assert all(item["provider"] == "cpam" for item in payload["items"])


def test_service_detail_404() -> None:
    response = client.get("/services/edf/not-there")
    assert response.status_code == 404


def test_monopoly_cards_shape() -> None:
    response = client.get("/monopoly/cards")
    assert response.status_code == 200
    payload = response.json()
    assert payload["items"]
    first = payload["items"][0]
    assert {"id", "provider", "title", "card_type", "amount_eur", "text"} <= set(first.keys())


def test_airbnb_api() -> None:
    response = client.get("/services", params={"provider": "airbnb"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["items"][0]["provider"] == "airbnb"
