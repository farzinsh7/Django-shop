from django.core import exceptions
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    View,
)
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from review.models import Review, ReviewStatusType
from django.db.models import Count


class ProductGridView(ListView):
    template_name = "shop/product-grid.html"
    paginate_by = 6

    def get_paginate_by(self, queryset):

        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset = models.Product.objects.prefetch_related("category").filter(
            status=models.StatusType.publish.value)
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
        if min_price := self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)
        if max_price := self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except exceptions.FieldError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_items'] = self.get_queryset().count()
        if self.request.user.is_authenticated:
            context['wishlist_products'] = models.WishlistProducts.objects.filter(
                user=self.request.user
            ).values_list('product__id', flat=True)
        else:
            context['wishlist_products'] = []
        context['categories'] = models.ProductCategory.objects.all()
        return context


class ProductDetailView(DetailView):
    model = models.Product
    queryset = models.Product.objects.filter(
        status=models.StatusType.publish.value)
    template_name = "shop/product-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        if self.request.user.is_authenticated:
            context['wishlist_products'] = models.WishlistProducts.objects.filter(
                user=self.request.user
            ).values_list('product__id', flat=True)
        else:
            context['wishlist_products'] = []

        context['reviews'] = Review.objects.filter(
            product=product, status=ReviewStatusType.accepted.value
        )

        ratings = Review.objects.filter(
            product=product, status=ReviewStatusType.accepted.value
        ).values('rate').annotate(count=Count('id'))

        rating_counts = {rate: 0 for rate in range(5, 0, -1)}

        total_ratings = sum(rating['count'] for rating in ratings)

        for rating in ratings:
            rating_counts[rating['rate']] = {
                'count': rating['count'],
                'percent': (rating['count'] / total_ratings) * 100 if total_ratings > 0 else 0
            }

        context['rating_counts'] = rating_counts

        return context


class AddOrRemoveWishlistView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'درخواست نامعتبر'}, status=400)

        product_id = request.POST.get('product_id')
        message = ""

        if product_id:
            try:
                whislist_item = models.WishlistProducts.objects.get(
                    user=request.user, product__id=product_id)
                whislist_item.delete()
                message = "محصول از لیست علاقه مندی حذف گردید."
            except models.WishlistProducts.DoesNotExist:
                models.WishlistProducts.objects.create(
                    user=request.user, product_id=product_id)
                message = "محصول مورد نظر با موفقیت به لیست علاقه مندی اضافه گردید."

        return JsonResponse({"message": message})
