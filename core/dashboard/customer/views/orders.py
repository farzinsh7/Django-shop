from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from dashboard.permissions import HasCustomerAccessPermission
from dashboard.customer.forms import UserAddressForm
from order.models import UserAddress
from django.core import exceptions
from order.models import Order


class CustomerOrdersListView(LoginRequiredMixin, HasCustomerAccessPermission, ListView):
    template_name = "dashboard/customer/orders/order-list.html"

    def get_queryset(self):
        queryset = Order.objects.prefetch_related(
            'order_items__product').filter(user=self.request.user)
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except exceptions.FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_orders'] = self.get_queryset().count()
        return context


class CustomerOrderDetailView(LoginRequiredMixin, HasCustomerAccessPermission, DetailView):
    model = Order
    queryset = Order.objects.all()
    template_name = "dashboard/customer/orders/order-detail.html"
