import decimal
from datetime import date

from django.core.serializers.json import DjangoJSONEncoder

from .models import Rate


class DecimalAsFloatJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)


def calculate_exchange(amount, pair):
    today = date.today()
    if pair == "UAHtoUSD":
        rate = (
            Rate.objects.filter(date=today, currency_a="USD").order_by("sell").first()
        )
        value = rate.sell
        result = round(amount / value, 2)
    elif pair == "UAHtoEUR":
        rate = (
            Rate.objects.filter(date=today, currency_a="EUR").order_by("sell").first()
        )
        value = rate.sell
        result = round(amount / value, 2)
    elif pair == "USDtoUAH":
        rate = (
            Rate.objects.filter(date=today, currency_a="USD").order_by("-buy").first()
        )
        value = rate.buy
        result = round(amount * value, 2)
    elif pair == "EURtoUAH":
        rate = (
            Rate.objects.filter(date=today, currency_a="EUR").order_by("-buy").first()
        )
        value = rate.buy
        result = round(amount * value, 2)
    else:
        rate = None
        value = None
        result = None
    vendor = rate.vendor
    return vendor, value, result
