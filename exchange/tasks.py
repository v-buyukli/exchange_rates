import datetime

from celery import shared_task

from .exchange_provider import Exchange, MonoExchange, PrivatExchange
from .models import Rate


@shared_task
def start_exchange(vendor, currency_a, currency_b):
    current_date = datetime.date.today()
    is_rate_exists = Rate.objects.filter(
        date=current_date, vendor=vendor, currency_a=currency_a, currency_b=currency_b
    ).exists()

    if is_rate_exists:
        print(f"Rate already exists for {current_date} {vendor} {currency_a} {currency_b}")
        return

    if vendor == "mono":
        exchange = MonoExchange(vendor, currency_a, currency_b)
    elif vendor == "privat":
        exchange = PrivatExchange(vendor, currency_a, currency_b)
    else:
        exchange = Exchange(vendor, currency_a, currency_b)
    exchange.get_rate()

    Rate.objects.get_or_create(
        date=current_date,
        vendor=vendor,
        currency_a=currency_a,
        currency_b=currency_b,
        defaults={"sell": exchange.pair.sell, "buy": exchange.pair.buy},
    )
