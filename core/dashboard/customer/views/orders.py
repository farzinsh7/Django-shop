from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from dashboard.permissions import HasCustomerAccessPermission
from django.core import exceptions
from order.models import Order, OrderStatus
from order.utils import calculate_tax, calculate_shipping
from decimal import Decimal


class CustomerOrdersListView(LoginRequiredMixin, HasCustomerAccessPermission, ListView):
    template_name = "dashboard/customer/orders/order-list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = Order.objects.prefetch_related(
            'order_items__product').filter(user=self.request.user).order_by('-created_at')
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(id__icontains=search_q)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_orders'] = self.get_queryset().count()
        return context


class CustomerOrderDetailView(LoginRequiredMixin, HasCustomerAccessPermission, DetailView):
    template_name = "dashboard/customer/orders/order-detail.html"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CustomerOrderInvoiceView(LoginRequiredMixin, HasCustomerAccessPermission, DetailView):
    template_name = "dashboard/customer/orders/order-invoice.html"

    def get_queryset(self):
        return Order.objects.filter(status=OrderStatus.deliverd.value).filter(user=self.request.user)

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
