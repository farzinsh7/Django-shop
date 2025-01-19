from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserAddress


class OrderCheckOutView(LoginRequiredMixin, TemplateView):
    template_name = "order/checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = UserAddress.objects.filter(
            user=self.request.user)
        return context
