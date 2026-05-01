from unittest.mock import Mock, patch

import httpx
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ecosystem() -> None:
    response = client.get("/ecosystem")
    assert response.status_code == 200
    payload = response.json()
    assert "services" in payload
    services = payload["services"]
    assert len(services) == 10
    ids = {s["id"] for s in services}
    assert "franceconnect" in ids
    assert "save_service" in ids
    assert "wallet" in ids
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


def test_payment_link_success() -> None:
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"url": "https://buy.stripe.com/test_link_123"}

    with patch("app.services.payments.httpx.post", return_value=mock_response) as mocked_post:
        response = client.post(
            "/payments/link",
            json={
                "app": "wallet",
                "context": "topup",
                "reference_id": "resv_123",
                "metadata": {"listingId": "listing_1"},
                "amount_hint_eur": 12.5,
                "amount_hint_cents": 1250,
            },
        )

    assert response.status_code == 200
    assert response.json() == {"url": "https://buy.stripe.com/test_link_123"}
    forwarded = mocked_post.call_args.kwargs["json"]
    assert forwarded["app"] == "wallet"
    assert forwarded["context"] == "topup"
    assert forwarded["amount_hint_eur"] == 12.5
    assert forwarded["amount_hint_cents"] == 1250


def test_payment_link_timeout() -> None:
    with patch(
        "app.services.payments.httpx.post",
        side_effect=httpx.TimeoutException("timeout"),
    ):
        response = client.post(
            "/payments/link",
            json={"app": "web", "context": "transfer", "reference_id": "tx_123"},
        )

    assert response.status_code == 502
    assert response.json()["detail"] == "Timeout vers stripe-monopoly"


def test_payment_link_upstream_error() -> None:
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {"detail": "Stripe indisponible"}

    with patch("app.services.payments.httpx.post", return_value=mock_response):
        response = client.post(
            "/payments/link",
            json={"app": "declaration", "context": "tax", "reference_id": "decl_001"},
        )

    assert response.status_code == 502
    assert response.json()["detail"] == "Stripe indisponible"


def test_payment_link_missing_url() -> None:
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"ok": True}

    with patch("app.services.payments.httpx.post", return_value=mock_response):
        response = client.post(
            "/payments/link",
            json={"app": "sncf_connect", "context": "ticket", "reference_id": "tic_42"},
        )

    assert response.status_code == 502
    assert response.json()["detail"] == "URL manquante dans la reponse stripe-monopoly"
