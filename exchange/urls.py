from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("exchange-rates/", views.exchange_rates, name="exchange-rates"),
]
