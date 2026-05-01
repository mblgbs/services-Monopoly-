from __future__ import annotations

import os
from dataclasses import dataclass

import httpx

from ..schemas import PaymentLinkRequest


@dataclass
class PaymentProxyError(Exception):
    detail: str

    def __str__(self) -> str:
        return self.detail


def _stripe_base_url() -> str:
    return os.getenv("STRIPE_MONOPOLY_BASE_URL", "http://127.0.0.1:8006").strip().rstrip("/")


def _extract_error_detail(response: httpx.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        payload = None

    if isinstance(payload, dict):
        detail = payload.get("detail") or payload.get("error")
        if isinstance(detail, str) and detail.strip():
            return detail.strip()

    return f"stripe-monopoly a renvoye HTTP {response.status_code}"


def create_payment_link(request: PaymentLinkRequest) -> str:
    url = f"{_stripe_base_url()}/payment-links"
    payload = {
        "app": request.app,
        "context": request.context,
        "reference_id": request.reference_id,
        "metadata": request.metadata or {},
        "amount_hint_eur": request.amount_hint_eur,
        "amount_hint_cents": request.amount_hint_cents,
    }

    try:
        response = httpx.post(url, json=payload, timeout=5.0)
    except httpx.TimeoutException as exc:
        raise PaymentProxyError("Timeout vers stripe-monopoly") from exc
    except httpx.HTTPError as exc:
        raise PaymentProxyError("Erreur reseau vers stripe-monopoly") from exc

    if response.status_code >= 400:
        raise PaymentProxyError(_extract_error_detail(response))

    try:
        data = response.json()
    except ValueError as exc:
        raise PaymentProxyError("Reponse JSON invalide de stripe-monopoly") from exc

    payment_url = data.get("url") if isinstance(data, dict) else None
    if not isinstance(payment_url, str) or not payment_url.strip():
        raise PaymentProxyError("URL manquante dans la reponse stripe-monopoly")

    return payment_url
