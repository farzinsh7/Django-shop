from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from dashboard.permissions import HasCustomerAccessPermission
from shop.models import WishlistProducts, StatusType
from django.core import exceptions


class CustomerWishlistListView(LoginRequiredMixin, HasCustomerAccessPermission, ListView):
    template_name = "dashboard/customer/wishlists/wishlist-list.html"
    paginate_by = 5

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset = WishlistProducts.objects.filter(
            user=self.request.user).filter(product__status=StatusType.publish.value)
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(product__title__icontains=search_q)
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


class CustomerWishlistDeleteView(LoginRequiredMixin, HasCustomerAccessPermission, SuccessMessageMixin, DeleteView):
    http_method_names = ["post"]
    success_message = "محصول انتخابی با موفقیت حذف گردید."
    success_url = reverse_lazy("dashboard:customer:wishlist-list")

    def get_queryset(self):
        return WishlistProducts.objects.filter(user=self.request.user)
