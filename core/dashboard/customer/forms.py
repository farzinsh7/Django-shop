from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from django import forms
from accounts.models import Profile


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
