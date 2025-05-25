import datetime
import json
import pathlib

import pytest
import responses
from django.conf import settings
from django.core.management import call_command
from freezegun import freeze_time

from .exchange_provider import (
    MonoExchange,
    PrivatExchange,
    RateAPIExchange,
    UniversalExchange,
    VkurseExchange,
)
from .views import exchange_rates


root = pathlib.Path(__file__).parent


@pytest.fixture
def mocked():
    def inner(file_name):
        return json.load(open(root / "fixtures" / file_name))

    return inner


@responses.activate
def test_exchange_mono(mocked):
    mocked_response = mocked("mono_response.json")
    responses.get(
        settings.EXCHANGE_URLS["MONO"],
        json=mocked_response,
    )
    e = MonoExchange("mono", "USD", "UAH")
    e.get_rate()
    assert e.pair.buy == 36.65
    assert e.pair.sell == 37.4406


@responses.activate
def test_privat_rate(mocked):
    mocked_response = mocked("privat_response.json")
    date = datetime.date(2023, 5, 14)
    url = f"{settings.EXCHANGE_URLS['PRIVAT']}&date={date.strftime('%d.%m.%Y')}"
    responses.get(
        url,
        json=mocked_response,
    )
    e = PrivatExchange("privat", "USD", "UAH", date)
    e.get_rate()
    assert e.pair.buy == 37.1
    assert e.pair.sell == 37.6


@responses.activate
def test_exchange_universal(mocked):
    mocked_response = mocked("universal_response.json")
    responses.get(
        settings.EXCHANGE_URLS["UNIVERSAL"],
        json=mocked_response,
    )
    e = UniversalExchange("universal", "USD", "UAH")
    e.get_rate()
    assert e.pair.buy == 37.05
    assert e.pair.sell == 37.55


@responses.activate
def test_vkurse_rate(mocked):
    mocked_response = mocked("vkurse_response.json")
    responses.get(
        settings.EXCHANGE_URLS["VKURSE"],
        json=mocked_response,
    )
    e = VkurseExchange("vkurse", "USD", "UAH")
    e.get_rate()
    assert e.pair.buy == 37.6
    assert e.pair.sell == 37.8


@responses.activate
def test_rateapi_rate(mocked):
    mocked_response_uah = mocked("rateapi_response_uah_response.json")
    mocked_response_usd = mocked("rateapi_response_usd_response.json")
    mocked_response_eur = mocked("rateapi_response_eur_response.json")

    api_key = settings.RATE_API_KEY
    base_url = settings.EXCHANGE_URLS["RATE_API_BASE"]
    responses.get(
        f"{base_url}/{api_key}/latest/UAH",
        json=mocked_response_uah,
    )
    responses.get(
        f"{base_url}/{api_key}/latest/USD",
        json=mocked_response_usd,
    )
    responses.get(
        f"{base_url}/{api_key}/latest/EUR",
        json=mocked_response_eur,
    )

    e = RateAPIExchange("rateapi", "USD", "UAH")
    e.get_rate()
    assert e.pair.buy == 36.9355
    assert e.pair.sell == 36.9413


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "db_init.yaml")


@freeze_time("2023-01-01")
@pytest.mark.django_db
def test_exchange_rates_view(mocked):
    response = exchange_rates(None)
    assert json.loads(response.content) == mocked("exchange_rates_view.json")
