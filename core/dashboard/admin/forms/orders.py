from django import forms
from django.utils.translation import gettext_lazy as _
from order.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'status',
            'payment',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs['class'] = "form-select"
        self.fields['payment'].widget.attrs['class'] = "form-control"
