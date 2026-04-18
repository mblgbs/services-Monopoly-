from __future__ import annotations

from ..schemas import MonopolyCard, Provider, ServiceOffer

BONUS_CATEGORIES = {"sante", "aide", "logement"}  # Airbnb as bonus


def to_card(offer: ServiceOffer) -> MonopolyCard:
    card_type: str
    amount_eur: int
    if offer.category in BONUS_CATEGORIES:
        card_type = "bonus"
        amount_eur = round(offer.monthly_price_eur)
        text = f"Subvention {offer.provider.upper()}: recevez {amount_eur} EUR"
    else:
        card_type = "charge"
        amount_eur = round(offer.monthly_price_eur)
        text = f"Abonnement {offer.provider.upper()}: payez {amount_eur} EUR"

    return MonopolyCard(
        id=f"card-{offer.provider}-{offer.id}",
        provider=offer.provider,
        title=offer.name,
        card_type=card_type,
        amount_eur=amount_eur,
        text=text,
    )


def to_cards(offers: list[ServiceOffer], provider: Provider | None = None) -> list[MonopolyCard]:
    if provider is not None:
        offers = [offer for offer in offers if offer.provider == provider]
    return [to_card(offer) for offer in offers]
