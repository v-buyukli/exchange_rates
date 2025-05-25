import abc
from dataclasses import dataclass
from enum import Enum

import requests
from django.conf import settings
from fake_useragent import UserAgent


class ExchangeCodes(Enum):
    USD = 840
    EUR = 978
    UAH = 980


@dataclass(frozen=True)
class SellBuy:
    sell: float
    buy: float


class Exchange(abc.ABC):
    def __init__(self, vendor, currency_a, currency_b):
        self.vendor = vendor
        self.currency_a = currency_a
        self.currency_b = currency_b
        self.pair = None

    @abc.abstractmethod
    def get_rate(self):
        raise NotImplementedError("Method get_rate() is not implemented")


class MonoExchange(Exchange):
    def get_rate(self):
        a_code = ExchangeCodes[self.currency_a].value
        b_code = ExchangeCodes[self.currency_b].value
        r = requests.get(settings.EXCHANGE_URLS["MONO"])
        r.raise_for_status()

        for rate in r.json():
            if rate["currencyCodeA"] == a_code and rate["currencyCodeB"] == b_code:
                self.pair = SellBuy(rate["rateSell"], rate["rateBuy"])
                return


class PrivatExchange(Exchange):
    def __init__(self, vendor, currency_a, currency_b, date):
        super().__init__(vendor, currency_a, currency_b)
        self.date = date.strftime("%d.%m.%Y")

    def get_rate(self):
        base_url = settings.EXCHANGE_URLS["PRIVAT"]
        url = f"{base_url}&date={self.date}"
        r = requests.get(url)
        r.raise_for_status()

        for rate in r.json().get("exchangeRate", []):
            if (
                rate.get("currency") == self.currency_a
                and rate.get("baseCurrency") == self.currency_b
            ):
                self.pair = SellBuy(rate["saleRate"], rate["purchaseRate"])
                return


class UniversalExchange(Exchange):
    def get_rate(self):
        headers = {"User-Agent": UserAgent().chrome}
        url = settings.EXCHANGE_URLS["UNIVERSAL"]
        r = requests.get(url, headers=headers)
        r.raise_for_status()

        for rate in r.json():
            if rate["currency"] == self.currency_a:
                self.pair = SellBuy(float(rate["sale"]), float(rate["buy"]))
                return


class VkurseExchange(Exchange):
    def get_rate(self):
        url = settings.EXCHANGE_URLS["VKURSE"]
        r = requests.get(url)
        r.raise_for_status()
        rate = r.json()

        if self.currency_a == "USD":
            self.pair = SellBuy(
                float(rate["Dollar"]["sale"]),
                float(rate["Dollar"]["buy"]),
            )
            return
        elif self.currency_a == "EUR":
            self.pair = SellBuy(
                float(rate["Euro"]["sale"]),
                float(rate["Euro"]["buy"]),
            )
            return


class RateAPIExchange(Exchange):
    def get_rate(self):
        base_url = settings.EXCHANGE_URLS["RATE_API_BASE"]
        api_key = settings.RATE_API_KEY

        urls = {
            "UAH": f"{base_url}/{api_key}/latest/UAH",
            "USD": f"{base_url}/{api_key}/latest/USD",
            "EUR": f"{base_url}/{api_key}/latest/EUR",
        }

        responses = {k: requests.get(v) for k, v in urls.items()}
        for response in responses.values():
            response.raise_for_status()

        rate_uah = responses["UAH"].json()
        rate_usd = responses["USD"].json()
        rate_eur = responses["EUR"].json()

        if self.currency_a == "USD":
            self.pair = SellBuy(
                round(1 / rate_uah["conversion_rates"]["USD"], 4),
                rate_usd["conversion_rates"]["UAH"],
            )
            return
        elif self.currency_a == "EUR":
            self.pair = SellBuy(
                round(1 / rate_uah["conversion_rates"]["EUR"], 4),
                rate_eur["conversion_rates"]["UAH"],
            )
            return
