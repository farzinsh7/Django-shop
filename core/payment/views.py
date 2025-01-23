from django.shortcuts import render
from django.views.generic import View
from .models import Payment, PaymentStatus
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from .zarinpal_client import ZarinPalSandBox


class PaymentVerifyView(View):

    def get(self, request, *args, **kwargs):
        authority_id = request.GET.get("Authority")
        status = request.GET.get("Status")

        payment_obj = get_object_or_404(Payment, authority_id=authority_id)
        zarinpal = ZarinPalSandBox()
        response = zarinpal.payment_verify(
            payment_obj.amount, payment_obj.authority_id)
        if status == "OK":
            payment_obj.ref_id = response['data']["ref_id"]
            payment_obj.response_code = response['data']["code"]
            payment_obj.status = PaymentStatus.success.value
            payment_obj.response_json = response
            payment_obj.save()
            return redirect(reverse_lazy("order:completed"))
        else:
            # payment_obj.ref_id = response['data']["ref_id"]
            payment_obj.response_code = response['errors']["code"]
            payment_obj.status = PaymentStatus.failed.value
            payment_obj.response_json = response
            payment_obj.save()
            return redirect(reverse_lazy("order:failed"))
