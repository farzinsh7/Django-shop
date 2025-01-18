from django import forms
from .models import ContactUsModel


class ContactFormClass(forms.ModelForm):
    class Meta:
        model = ContactUsModel
        fields = ('first_name', 'last_name', 'email', 'phone', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = "form-control form-control-lg"
        self.fields['first_name'].widget.attrs['placeholder'] = "نام خانوادگی"
        self.fields['last_name'].widget.attrs['class'] = "form-control form-control-lg"
        self.fields['last_name'].widget.attrs['placeholder'] = "نام"
        self.fields['phone'].widget.attrs['class'] = "form-control form-control-lg"
        self.fields['phone'].widget.attrs['placeholder'] = "yourmail@gmail.com"
        self.fields['email'].widget.attrs['class'] = "form-control form-control-lg"
        self.fields['email'].widget.attrs['placeholder'] = "+9891200000"
        self.fields['description'].widget.attrs['class'] = "form-control form-control-lg"
        self.fields['description'].widget.attrs['placeholder'] = "توضیحات خود را وارد نمایید"
