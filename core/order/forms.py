from django import forms
from .models import UserAddress, Coupon
from django.utils import timezone


class CheckOutForm(forms.Form):
    address_id = forms.IntegerField(required=True)
    coupon = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CheckOutForm, self).__init__(*args, **kwargs)

    def clean_address_id(self):
        address_id = self.cleaned_data.get('address_id')

        user = self.request.user
        try:
            address = UserAddress.objects.get(id=address_id, user=user)
        except UserAddress.DoesNotExist:
            raise forms.ValidationError(
                "Invalid address for the requested user.")

        return address

    def clean_coupon(self):
        code = self.cleaned_data.get('coupon')

        if not code:
            return None

        user = self.request.user
        coupon = None

        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            raise forms.ValidationError("کد تخفیف معتبر نمی باشد!")

        if coupon:
            if coupon.used_by.count() >= coupon.max_limit_usage:
                raise forms.ValidationError("خطای محدودیت در تعداد استفاده")

            if coupon.expiration_date and coupon.expiration_date < timezone.now():
                raise forms.ValidationError("کد تخفیف منقضی شده است")

            if user in coupon.used_by.all():
                raise forms.ValidationError(
                    "این کد تخفیف قبلا توسط شما استفاده شده است.")

        return coupon
