import abc
from dataclasses import dataclass
from enum import Enum

import requests
from django.conf import settings


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
        r = requests.get("https://api.monobank.ua/bank/currency")
        r.raise_for_status()

        for rate in r.json():
            currency_code_a = rate["currencyCodeA"]
            currency_code_b = rate["currencyCodeB"]
            if currency_code_a == a_code and currency_code_b == b_code:
                self.pair = SellBuy(rate["rateSell"], rate["rateBuy"])
                return


class PrivatExchange(Exchange):
    def __init__(self, vendor, currency_a, currency_b, date):
        super().__init__(vendor, currency_a, currency_b)
        self.date = date.strftime("%d.%m.%Y")

    def get_rate(self):
        r = requests.get(f"https://api.privatbank.ua/p24api/exchange_rates?json&date={self.date}&coursid=11")
        r.raise_for_status()

        for rate in r.json()["exchangeRate"]:
            if rate["currency"] == self.currency_a and rate["baseCurrency"] == self.currency_b:
                self.pair = SellBuy(rate["saleRate"], rate["purchaseRate"])
                return


class UniversalExchange(Exchange):
    def get_rate(self):
        r = requests.get("https://www.universalbank.com.ua/api/rates/json")
        r.raise_for_status()

        for rate in r.json():
            if rate["currency"] == self.currency_a:
                self.pair = SellBuy(float(rate["sale"]), float(rate["buy"]))
                return


class VkurseExchange(Exchange):
    def get_rate(self):
        r = requests.get("https://vkurse.dp.ua/course.json")
        r.raise_for_status()
        rate = r.json()

        if self.currency_a == "USD":
            self.pair = SellBuy(float(rate["Dollar"]["sale"]), float(rate["Dollar"]["buy"]))
            return
        elif self.currency_a == "EUR":
            self.pair = SellBuy(float(rate["Euro"]["sale"]), float(rate["Euro"]["buy"]))
            return


class RateAPIExchange(Exchange):
    def get_rate(self):
        base_url = "https://v6.exchangerate-api.com/v6"
        api_key = settings.RATE_API_KEY

        url_base_uah = f"{base_url}/{api_key}/latest/UAH"
        url_base_usd = f"{base_url}/{api_key}/latest/USD"
        url_base_eur = f"{base_url}/{api_key}/latest/EUR"
        r_uah = requests.get(url_base_uah)
        r_usd = requests.get(url_base_usd)
        r_eur = requests.get(url_base_eur)
        r_uah.raise_for_status()
        r_usd.raise_for_status()
        r_eur.raise_for_status()
        rate_uah = r_uah.json()
        rate_usd = r_usd.json()
        rate_eur = r_eur.json()

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
