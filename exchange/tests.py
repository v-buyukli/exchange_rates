import datetime
import json
import pathlib

import pytest
import responses
from django.conf import settings

from .exchange_provider import (MonoExchange, PrivatExchange, RateAPIExchange,
                                UniversalExchange, VkurseExchange)

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
        "https://api.monobank.ua/bank/currency",
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
    responses.get(
        f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date.strftime('%d.%m.%Y')}&coursid=11",
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
        "https://www.universalbank.com.ua/api/rates/json",
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
        "https://vkurse.dp.ua/course.json",
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
    responses.get(
        f"https://v6.exchangerate-api.com/v6/{api_key}/latest/UAH",
        json=mocked_response_uah,
    )
    responses.get(
        f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD",
        json=mocked_response_usd,
    )
    responses.get(
        f"https://v6.exchangerate-api.com/v6/{api_key}/latest/EUR",
        json=mocked_response_eur,
    )

    e = RateAPIExchange("rateapi", "USD", "UAH")
    e.get_rate()
    assert e.pair.buy == 36.9355
    assert e.pair.sell == 36.9413
