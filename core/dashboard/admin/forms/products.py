from django import forms
from django.utils.translation import gettext_lazy as _
from shop.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "title",
            "slug",
            "category",
            "image",
            "description",
            "short_description",
            "stock",
            "status",
            "sku",
            "price",
            "discount_percent",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = "form-control"
        self.fields['slug'].widget.attrs['class'] = "form-control"
        self.fields['category'].widget.attrs['class'] = "form-select"
        self.fields['image'].widget.attrs['class'] = "form-control"
        self.fields['description'].widget.attrs['class'] = "form-control"
        self.fields['short_description'].widget.attrs['class'] = "form-control"
        self.fields['stock'].widget.attrs['class'] = "form-control"
        self.fields['stock'].widget.attrs['type'] = "number"
        self.fields['status'].widget.attrs['class'] = "form-select"
        self.fields['sku'].widget.attrs['class'] = "form-control"
        self.fields['price'].widget.attrs['class'] = "form-control"
        self.fields['discount_percent'].widget.attrs['class'] = "form-control"
        self.fields['discount_percent'].widget.attrs['type'] = "number"
