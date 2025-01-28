from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, DetailView
from dashboard.admin.forms import OrderForm
from dashboard.permissions import HasAdminAccessPermission
from django.contrib.messages.views import SuccessMessageMixin
from order.models import Order, OrderStatus
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from order.utils import calculate_tax, calculate_shipping
from decimal import Decimal


class AdminOrderListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    template_name = "dashboard/admin/orders/order-list.html"
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset = Order.objects.prefetch_related('user').all()
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(id__icontains=search_q)
        if status := self.request.GET.get("status"):
            queryset = queryset.filter(status=status)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except exceptions.FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_items'] = self.get_queryset().count()
        context['statuses'] = OrderStatus.choices

        return context


class AdminOrderEditView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView):
    queryset = Order.objects.all()
    template_name = "dashboard/admin/orders/order-edit.html"
    form_class = OrderForm
    success_message = "بروزرسانی سفارش با موفقیت انجام شد."

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:order-edit", kwargs={"pk": self.get_object().pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order = self.object

        total_price = sum(
            item.price * item.quantity for item in order.order_items.all())

        # Apply coupon discount if available
        discount_amount = 0
        if order.coupon_at_order:
            discount_amount = round(
                total_price * Decimal(order.coupon_at_order) / 100)
            total_price -= discount_amount

        context['discount_amount'] = discount_amount

        return context


class AdminOrderInvoiceView(LoginRequiredMixin, HasAdminAccessPermission, DetailView):
    template_name = "dashboard/customer/orders/order-invoice.html"

    def get_queryset(self):
        return Order.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order = self.object
        coupon = order.coupon

        total_price = sum(
            item.price * item.quantity for item in order.order_items.all())

        # Apply coupon discount if available
        discount_amount = 0
        if order.coupon_at_order:
            discount_amount = round(
                total_price * Decimal(order.coupon_at_order) / 100)
            total_price -= discount_amount

        total_tax = calculate_tax(total_price)
        shipping_cost = calculate_shipping(total_price)

        context['discount_amount'] = discount_amount
        context['discount_percent'] = order.coupon_at_order
        context['coupon'] = coupon
        context['shipping_cost'] = shipping_cost
        context['total_tax'] = total_tax

        return context
