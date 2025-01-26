from django.utils.translation import gettext_lazy as _
from django import forms
from order.models import UserAddress


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['title',
                  'address',
                  'state',
                  'city',
                  'zip_code'
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = "form-control"
        self.fields['address'].widget.attrs['class'] = "form-control"
        self.fields['state'].widget.attrs['class'] = "form-control"
        self.fields['city'].widget.attrs['class'] = "form-control"
        self.fields['zip_code'].widget.attrs['class'] = "form-control"
        self.fields['title'].widget.attrs['placeholder'] = "بطور مثال: شرکت"
        self.fields['address'].widget.attrs['placeholder'] = "شامل: خیابان، کوچه، پلاک، طبقه و واحد"
        self.fields['state'].widget.attrs['placeholder'] = "استان خود را وارد کنید"
        self.fields['city'].widget.attrs['placeholder'] = "شهر خود را وارد کنید"
        self.fields['zip_code'].widget.attrs['placeholder'] = "کد پستی آدرس مورد نظر"
