from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserAddress
from .forms import CheckOutForm
from cart.models import Cart


class OrderCheckOutView(LoginRequiredMixin, FormView):
    template_name = "order/checkout.html"
    form_class = CheckOutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get(user=self.request.user)
        context['addresses'] = UserAddress.objects.filter(
            user=self.request.user)
        context['total_price'] = cart.calculate_total_price()
        return context
