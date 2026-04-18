from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Provider = Literal["edf", "eau", "cpam", "box_tv", "airbnb"]


class ServiceOffer(BaseModel):
    id: str
    provider: Provider
    name: str
    category: str
    monthly_price_eur: float = Field(ge=0)
    description: str


class ServiceOfferList(BaseModel):
    items: list[ServiceOffer]


class MonopolyCard(BaseModel):
    id: str
    provider: Provider
    title: str
    card_type: Literal["charge", "bonus"]
    amount_eur: int = Field(ge=0)
    text: str


class MonopolyCardList(BaseModel):
    items: list[MonopolyCard]
