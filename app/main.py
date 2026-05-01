from __future__ import annotations

import logging

from fastapi import FastAPI, HTTPException, status

from .ecosystem import build_ecosystem_entries
from .schemas import (
    EcosystemResponse,
    EcosystemService,
    MonopolyCardList,
    PaymentLinkRequest,
    PaymentLinkResponse,
    Provider,
    ServiceOffer,
    ServiceOfferList,
)
from .services.catalog import CatalogNotFoundError, get_offer, list_offers
from .services.monopoly_adapter import to_cards
from .services.payments import PaymentProxyError, create_payment_link

app = FastAPI(title="Services Monopoly API")
logger = logging.getLogger(__name__)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "services-monopoly"}


@app.get("/ecosystem", response_model=EcosystemResponse)
def ecosystem() -> EcosystemResponse:
    entries = build_ecosystem_entries()
    return EcosystemResponse(services=[EcosystemService(**e) for e in entries])


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


@app.post("/payments/link", response_model=PaymentLinkResponse)
def payments_link(payload: PaymentLinkRequest) -> PaymentLinkResponse:
    logger.info(
        "payment_link_requested app=%s context=%s reference_id=%s",
        payload.app,
        payload.context,
        payload.reference_id,
    )
    try:
        url = create_payment_link(payload)
    except PaymentProxyError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
    return PaymentLinkResponse(url=url)
