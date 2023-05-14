import datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .services import DecimalAsFloatJSONEncoder
from .models import Rate
from .forms import ExchangeForm, ExchangePair


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
    if request.method == 'POST':
        form = ExchangeForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            pair = request.POST['pair']
            return exchange_result(request, amount, pair)
    else:
        form = ExchangeForm()
    return render(request, "exchange.html", {"form": form})


def exchange_result(request, amount, pair):
    context = {
        "amount": amount,
        "pair": pair
    }
    return render(request, "exchange_result.html", context)
