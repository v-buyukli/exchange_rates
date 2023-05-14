from enum import Enum

from django import forms
from django.core.exceptions import ValidationError


class ExchangePair(Enum):
    UAHtoUSD = "UAH-USD"
    UAHtoEUR = "UAH-EUR"
    USDtoUAH = "USD-UAH"
    EURtoUAH = "EUR-UAH"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class ExchangeForm(forms.Form):
    amount = forms.IntegerField(min_value=1)
    pair = forms.ChoiceField(
        label="Currency from-to",
        choices=ExchangePair.choices(),
        widget=forms.RadioSelect(),
    )

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if not isinstance(amount, int) and amount < 1:
            raise ValidationError("Amount must be a positive integer")
        return amount
