from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from django import forms
from accounts.models import Profile
from order.models import UserAddress


class CustomerPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        "password_incorrect": _(
            "رمز عبور فعلی شما به درستی وارد نشده است. لطفا دوباره وارد کنید."
        ),
        "password_mismatch": _("فیلدهای رمز عبور جدید با هم برابر نیستند!"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = "form-control"
        self.fields['new_password1'].widget.attrs['class'] = "form-control"
        self.fields['new_password2'].widget.attrs['class'] = "form-control"
        self.fields['old_password'].widget.attrs['placeholder'] = "رمز عبور فعلی را وارد کنید."
        self.fields['new_password1'].widget.attrs['placeholder'] = "رمز عبور جدید را وارد کنید."
        self.fields['new_password2'].widget.attrs['placeholder'] = "مجدد رمز عبور جدید را وارد کنید."


class CustomerProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "phone_number",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = "form-control"
        self.fields['last_name'].widget.attrs['class'] = "form-control"
        self.fields['phone_number'].widget.attrs['class'] = "form-control"
        self.fields['first_name'].widget.attrs['placeholder'] = "نام"
        self.fields['last_name'].widget.attrs['placeholder'] = "نام خانوادگی"
        self.fields['phone_number'].widget.attrs['placeholder'] = "شماره همراه"


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
