from django import forms
from django.utils.translation import gettext_lazy as _
from review.models import Review


class AdminReviewForm(forms.ModelForm):
    RATE_CHOICES = [(i, i) for i in range(1, 6)]

    class Meta:
        model = Review
        fields = [
            "description",
            "status",
            "rate",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['class'] = "form-control"
        self.fields['status'].widget.attrs['class'] = "form-select"
        self.fields['rate'] = forms.ChoiceField(
            choices=self.RATE_CHOICES,
            widget=forms.Select(attrs={'class': 'form-select'})
        )
