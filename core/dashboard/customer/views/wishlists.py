from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from dashboard.permissions import HasCustomerAccessPermission
from shop.models import WishlistProducts, Product
from django.core import exceptions
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


class CustomerWishlistListView(LoginRequiredMixin, HasCustomerAccessPermission, ListView):
    template_name = "dashboard/customer/wishlists/wishlist-list.html"
    paginate_by = 5

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset = WishlistProducts.objects.filter(user=self.request.user)
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


class AddToWishlistView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'درخواست نامعتبر'}, status=400)

        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        # Check if the product is already in the wishlist
        if WishlistProducts.objects.filter(user=request.user, product=product).exists():
            return JsonResponse({'success': False, 'message': 'این محصول در لیست علاقه مندی شما وجود دارد.'})
        else:
            WishlistProducts.objects.create(user=request.user, product=product)
            return JsonResponse({'success': True, 'message': 'محصول شما با موفقیت به لیست علاقه مندی اضافه گردید.'})
