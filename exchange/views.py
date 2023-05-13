import datetime

from django.http import JsonResponse

from .services import DecimalAsFloatJSONEncoder
from .models import Rate


def index(request):
    current_date = datetime.date.today()
    current_rates = Rate.objects.filter(date=current_date).all().values()
    return JsonResponse(
        {"current_rates": list(current_rates)}, encoder=DecimalAsFloatJSONEncoder
    )
