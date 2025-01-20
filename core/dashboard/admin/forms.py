from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile
from shop.models import Product
from order.models import Coupon


class AdminPasswordChangeForm(PasswordChangeForm):
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


class AdminProfileEditForm(forms.ModelForm):
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
