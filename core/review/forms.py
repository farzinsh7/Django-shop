from django import forms
from .models import Review
from shop.models import Product, StatusType


class SubmitReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product',
                  'rate',
                  'description',
                  ]

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')

        try:
            Product.objects.get(id=product.id, status=StatusType.publish.value)

        except Product.DoesNotExist:
            raise forms.ValidationError("این محصول وجود ندارد")

        return cleaned_data
