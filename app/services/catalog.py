from __future__ import annotations

import json
from pathlib import Path

from ..schemas import Provider, ServiceOffer

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PROVIDERS: tuple[Provider, ...] = ("edf", "eau", "cpam", "box_tv")


class CatalogNotFoundError(Exception):
    """Raised when an offer cannot be found."""


def _load_provider(provider: Provider) -> list[ServiceOffer]:
    file_path = DATA_DIR / f"{provider}.json"
    payload = json.loads(file_path.read_text(encoding="utf-8"))
    return [ServiceOffer(provider=provider, **entry) for entry in payload]


def list_offers(provider: Provider | None = None) -> list[ServiceOffer]:
    if provider is not None:
        return _load_provider(provider)

    items: list[ServiceOffer] = []
    for current in PROVIDERS:
        items.extend(_load_provider(current))
    return items


def get_offer(provider: Provider, offer_id: str) -> ServiceOffer:
    for item in _load_provider(provider):
        if item.id == offer_id:
            return item
    raise CatalogNotFoundError(f"Offer {offer_id!r} for {provider!r} not found")
