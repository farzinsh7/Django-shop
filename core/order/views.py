from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserAddress
from .forms import CheckOutForm
from cart.models import Cart
from .utils import calculate_tax, calculate_shipping


class OrderCheckOutView(LoginRequiredMixin, FormView):
    template_name = "order/checkout.html"
    form_class = CheckOutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            cart = Cart.objects.get(user=self.request.user)
        except Cart.DoesNotExist:
            context['error'] = "کارت پیدا نشد."
            return context

        context['addresses'] = UserAddress.objects.filter(
            user=self.request.user)

        total_price = cart.calculate_total_price()
        total_tax = calculate_tax(total_price)
        shipping_cost = calculate_shipping(total_price)

        context['shipping_cost'] = shipping_cost
        context['total_tax'] = total_tax
        context['total_price'] = total_price + total_tax + shipping_cost
        return context
