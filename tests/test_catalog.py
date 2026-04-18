from app.services.catalog import CatalogNotFoundError, get_offer, list_offers


def test_list_offers_all_providers() -> None:
    items = list_offers()
    assert len(items) == 8


def test_list_offers_by_provider() -> None:
    items = list_offers("edf")
    assert len(items) == 2
    assert all(item.provider == "edf" for item in items)


def test_get_offer_not_found() -> None:
    try:
        get_offer("eau", "unknown")
    except CatalogNotFoundError:
        assert True
    else:
        raise AssertionError("Expected CatalogNotFoundError")


def test_airbnb_provider():
    catalog = CatalogService()
    airbnb_offers = catalog.list_offers(provider="airbnb")
    assert len(airbnb_offers) > 0
    assert airbnb_offers[0].provider == "airbnb"
