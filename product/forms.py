from django import forms
from .models import Product
from django_select2.forms import Select2MultipleWidget


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'category': Select2MultipleWidget,
            'tag': Select2MultipleWidget,
            'attribute': Select2MultipleWidget,
        }