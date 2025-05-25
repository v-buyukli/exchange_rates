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
    mapping = {
        "UAHtoUSD": {"currency": "USD", "field": "sell", "operation": "divide"},
        "UAHtoEUR": {"currency": "EUR", "field": "sell", "operation": "divide"},
        "USDtoUAH": {"currency": "USD", "field": "buy", "operation": "multiply"},
        "EURtoUAH": {"currency": "EUR", "field": "buy", "operation": "multiply"},
    }

    config = mapping.get(pair)
    if not config:
        return None, None, None

    qs = Rate.objects.filter(date=today, currency_a=config["currency"])
    qs = qs.order_by(
        config["field"] if config["operation"] == "divide" else f"-{config['field']}"
    )
    rate = qs.first()

    if not rate:
        return None, None, None

    value = getattr(rate, config["field"])
    result = (
        round(amount / value, 2)
        if config["operation"] == "divide"
        else round(amount * value, 2)
    )

    return rate.vendor, value, result
