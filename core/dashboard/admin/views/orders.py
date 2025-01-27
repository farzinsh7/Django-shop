from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, DeleteView
from dashboard.admin.forms import ProductForm
from dashboard.permissions import HasAdminAccessPermission
from django.contrib.messages.views import SuccessMessageMixin
from order.models import Order
from django.core import exceptions
from django.utils.translation import gettext_lazy as _


class AdminOrderListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    template_name = "dashboard/admin/orders/order-list.html"
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset = Order.objects.all().order_by("-created_at")
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except exceptions.FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_items'] = self.get_queryset().count()
        return context


class AdminOrderEditView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView):
    queryset = Order.objects.all()
    template_name = "dashboard/admin/orders/order-edit.html"
    # form_class = ProductForm
    success_message = "بروزرسانی سفارش با موفقیت انجام شد."

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:order-edit", kwargs={"pk": self.get_object().pk})


class AdminOrderDeleteView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, DeleteView):
    queryset = Order.objects.all()
    template_name = "dashboard/admin/orders/order-delete.html"
    success_message = "سفارش شما با موفقیت حذف گردید."
    success_url = reverse_lazy("dashboard:admin:orders-list")
