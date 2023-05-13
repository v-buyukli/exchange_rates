import datetime
from django.shortcuts import render
from django.http import JsonResponse

from .services import DecimalAsFloatJSONEncoder
from .models import Rate


def index(request):
    text = "Exchange"
    return render(request, "index.html", {"text": text})


def exchange_rates(request):
    current_date = datetime.date.today()
    current_rates = Rate.objects.filter(date=current_date).all().values()
    return JsonResponse(
        {"current_rates": list(current_rates)}, encoder=DecimalAsFloatJSONEncoder
    )
