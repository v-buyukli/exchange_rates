import datetime
import json
import pathlib

import responses

from .exchange_provider import MonoExchange, PrivatExchange, VkurseExchange


root = pathlib.Path(__file__).parent


@responses.activate
def test_exchange_mono():
    mocked_response = json.load(open(root / "fixtures/mono_response.json"))
    responses.get(
        "https://api.monobank.ua/bank/currency",
        json=mocked_response,
    )
    e = MonoExchange("mono", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 37.4406


@responses.activate
def test_privat_rate():
    mocked_response = json.load(open(root / "fixtures/privat_response.json"))
    date = datetime.date(2023, 5, 14)
    responses.get(
        f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date.strftime('%d.%m.%Y')}&coursid=11",
        json=mocked_response,
    )
    e = PrivatExchange("privat", "USD", "UAH", date)
    e.get_rate()
    assert e.pair.sell == 37.6


@responses.activate
def test_vkurse_rate():
    mocked_response = json.load(open(root / "fixtures/vkurse_response.json"))
    responses.get(
        "https://vkurse.dp.ua/course.json",
        json=mocked_response,
    )
    e = VkurseExchange("vkurse", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 37.8
