from __future__ import annotations

import os
from typing import TypedDict


class EcosystemServiceDict(TypedDict):
    id: str
    name: str
    role: str
    base_url: str
    docs_hint: str


def _base_url(env_key: str, default: str) -> str:
    raw = os.getenv(env_key, default).strip()
    return raw.rstrip("/")


def _services_monopoly_base_url() -> str:
    explicit = os.getenv("SERVICES_MONOPOLY_BASE_URL", "").strip()
    if explicit:
        return explicit.rstrip("/")
    return _base_url("APP_BASE_URL", "http://127.0.0.1:8004")


def build_ecosystem_entries() -> list[EcosystemServiceDict]:
    """URLs documentaires pour scripts et clients ; aucun appel réseau."""
    return [
        {
            "id": "franceconnect",
            "name": "FranceConnect Monopoly",
            "role": "Mock OAuth / session (cookie)",
            "base_url": _base_url("FRANCECONNECT_BASE_URL", "http://127.0.0.1:8001"),
            "docs_hint": "FranceConnect-Monopoly/README.md",
        },
        {
            "id": "banque",
            "name": "Compte de Banque Monopoly",
            "role": "API comptes / transferts",
            "base_url": _base_url("BANK_API_BASE_URL", "http://127.0.0.1:8002"),
            "docs_hint": "compte-de-Banque-Monopoly-/README.md",
        },
        {
            "id": "declaration",
            "name": "Déclaration Monopoly",
            "role": "API cartes Chance / Communauté",
            "base_url": _base_url("DECLARATION_API_BASE_URL", "http://127.0.0.1:8003"),
            "docs_hint": "D-claration-Monopoly-/README.md",
        },
        {
            "id": "services",
            "name": "Services Monopoly",
            "role": "Catalogue offres + cartes Monopoly (cette API)",
            "base_url": _services_monopoly_base_url(),
            "docs_hint": "services-Monopoly-/README.md",
        },
        {
            "id": "web",
            "name": "Web Monopoly",
            "role": "Front multijoueur + API salles",
            "base_url": _base_url("WEB_MONOPOLY_BASE_URL", "http://127.0.0.1:3000"),
            "docs_hint": "Web-monopoly-/README.md",
        },
        {
            "id": "sncf_connect",
            "name": "SNCF Connect Monopoly",
            "role": "Mock OAuth + tokens Bearer / introspection",
            "base_url": _base_url("SNCF_CONNECT_BASE_URL", "http://127.0.0.1:8005"),
            "docs_hint": "sncf-connect-Monopoly/README.md",
        },
        {
            "id": "stripe",
            "name": "Stripe Monopoly",
            "role": "Checkout / Payment Links / webhooks",
            "base_url": _base_url("STRIPE_MONOPOLY_BASE_URL", "http://127.0.0.1:8006"),
            "docs_hint": "stripe-Monopoly/README.md",
        },
        {
            "id": "airbnb",
            "name": "Airbnb Monopoly",
            "role": "MVP Next.js (listings / réservations)",
            "base_url": _base_url("AIRBNB_MONOPOLY_BASE_URL", "http://127.0.0.1:3001"),
            "docs_hint": "airbnb-monopoly-/README.md",
        },
        {
            "id": "save_service",
            "name": "Save service",
            "role": "Stockage d'état partagé (optionnel)",
            "base_url": _base_url("SAVE_SERVICE_BASE_URL", "http://127.0.0.1:8010"),
            "docs_hint": "voir variables SAVE_SERVICE_* dans Web / FranceConnect / Banque",
        },
    ]
