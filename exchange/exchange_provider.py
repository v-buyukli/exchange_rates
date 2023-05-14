import abc
from dataclasses import dataclass
from enum import Enum

import requests


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
