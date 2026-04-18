from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


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
