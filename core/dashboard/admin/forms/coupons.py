from django import forms
from django.utils.translation import gettext_lazy as _
from order.models import Coupon


class AdminCouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = [
            "code",
            "description",
            "discount_percent",
            "max_limit_usage",
            "used_by",
            "expiration_date",
        ]
        widgets = {
            'expiration_date': forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['class'] = "form-control"
        self.fields['description'].widget.attrs['class'] = "form-control"
        self.fields['discount_percent'].widget.attrs['class'] = "form-control"
        self.fields['max_limit_usage'].widget.attrs['class'] = "form-control"
        self.fields['used_by'].widget.attrs['class'] = "form-control"
