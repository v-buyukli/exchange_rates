import datetime

from django.http import JsonResponse
from django.shortcuts import render

from .forms import ExchangeForm
from .models import Rate
from .services import DecimalAsFloatJSONEncoder, calculate_exchange


def index(request):
    context = "Exchange page"
    return render(request, "index.html", {"context": context})


def exchange_rates(request):
    current_date = datetime.date.today()
    current_rates = Rate.objects.filter(date=current_date).all().values()
    return JsonResponse(
        {"current_rates": list(current_rates)}, encoder=DecimalAsFloatJSONEncoder
    )


def exchange(request):
    if request.method == "POST":
        form = ExchangeForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            pair = request.POST["pair"]
            return exchange_result(request, amount, pair)
    else:
        form = ExchangeForm()
    return render(request, "exchange.html", {"form": form})


def exchange_result(request, amount, pair):
    vendor, rate, result = calculate_exchange(amount, pair)
    context = {
        "pair": pair,
        "amount": amount,
        "rate": rate,
        "vendor": vendor,
        "result": result,
    }
    return render(request, "exchange_result.html", context)
