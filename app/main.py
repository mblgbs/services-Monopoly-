from __future__ import annotations

from fastapi import FastAPI, HTTPException, status

from .schemas import MonopolyCardList, Provider, ServiceOffer, ServiceOfferList
from .services.catalog import CatalogNotFoundError, get_offer, list_offers
from .services.monopoly_adapter import to_cards

app = FastAPI(title="Services Monopoly API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "services-monopoly"}


@app.get("/services", response_model=ServiceOfferList)
def services(provider: Provider | None = None) -> ServiceOfferList:
    return ServiceOfferList(items=list_offers(provider))


@app.get("/services/{provider}", response_model=ServiceOfferList)
def services_by_provider(provider: Provider) -> ServiceOfferList:
    return ServiceOfferList(items=list_offers(provider))


@app.get("/services/{provider}/{offer_id}", response_model=ServiceOffer)
def service_detail(provider: Provider, offer_id: str) -> ServiceOffer:
    try:
        return get_offer(provider, offer_id)
    except CatalogNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@app.get("/monopoly/cards", response_model=MonopolyCardList)
def monopoly_cards(provider: Provider | None = None) -> MonopolyCardList:
    offers = list_offers(provider)
    return MonopolyCardList(items=to_cards(offers, provider))
