import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exchange_rates.settings")

app = Celery("exchange_rates")
time_period = crontab(minute=0, hour=5)

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "mono-USD-UAH": {
        "task": "exchange.tasks.start_exchange",
        "schedule": time_period,
        "args": ("mono", "USD", "UAH"),
    },
    "mono-EUR-UAH": {
        "task": "exchange.tasks.start_exchange",
        "schedule": time_period,
        "args": ("mono", "EUR", "UAH"),
    },
    "privat-USD-UAH": {
        "task": "exchange.tasks.start_exchange",
        "schedule": time_period,
        "args": ("privat", "USD", "UAH"),
    },
    "privat-EUR-UAH": {
        "task": "exchange.tasks.start_exchange",
        "schedule": time_period,
        "args": ("privat", "EUR", "UAH"),
    },
    "universal-USD-UAH": {
        "task": "exchange.tasks.start_exchange",
        "schedule": time_period,
        "args": ("universal", "USD", "UAH"),
    },
    "universal-EUR-UAH": {
        "task": "exchange.tasks.start_exchange",
        "schedule": time_period,
        "args": ("universal", "EUR", "UAH"),
    },
    "vkurse-USD-UAH": {
        "task": "exchange.tasks.start_exchange",
        "schedule": time_period,
        "args": ("vkurse", "USD", "UAH"),
    },
    "vkurse-EUR-UAH": {
        "task": "exchange.tasks.start_exchange",
        "schedule": time_period,
        "args": ("vkurse", "EUR", "UAH"),
    },
    "rateapi-USD-UAH": {
        "task": "exchange.tasks.start_exchange",
        "schedule": time_period,
        "args": ("rateapi", "USD", "UAH"),
    },
    "rateapi-EUR-UAH": {
        "task": "exchange.tasks.start_exchange",
        "schedule": time_period,
        "args": ("rateapi", "EUR", "UAH"),
    },
}
