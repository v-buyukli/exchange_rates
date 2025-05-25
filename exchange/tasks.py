import datetime
import logging

from celery import shared_task

from .exchange_provider import (
    Exchange,
    MonoExchange,
    PrivatExchange,
    RateAPIExchange,
    UniversalExchange,
    VkurseExchange,
)
from .models import Rate


logger = logging.getLogger(__name__)

EXCHANGE_CLASSES = {
    "mono": MonoExchange,
    "privat": PrivatExchange,
    "universal": UniversalExchange,
    "vkurse": VkurseExchange,
    "rateapi": RateAPIExchange,
}


@shared_task
def start_exchange(vendor, currency_a, currency_b):
    current_date = datetime.date.today()

    if Rate.objects.filter(
        date=current_date, vendor=vendor, currency_a=currency_a, currency_b=currency_b
    ).exists():
        logger.info(
            f"Rate already exists for {current_date} {vendor} {currency_a} {currency_b}"
        )
        return

    ExchangeClass = EXCHANGE_CLASSES.get(vendor, Exchange)
    if vendor == "privat":
        exchange = ExchangeClass(vendor, currency_a, currency_b, current_date)
    else:
        exchange = ExchangeClass(vendor, currency_a, currency_b)

    try:
        exchange.get_rate()
    except Exception as e:
        logger.error(f"Error while fetching rate from {vendor}: {e}")
        return

    if not exchange.pair:
        logger.warning(f"No rate found for {vendor} {currency_a}->{currency_b}")
        return

    Rate.objects.get_or_create(
        date=current_date,
        vendor=vendor,
        currency_a=currency_a,
        currency_b=currency_b,
        defaults={"sell": exchange.pair.sell, "buy": exchange.pair.buy},
    )
