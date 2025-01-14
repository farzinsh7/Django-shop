from django.core import exceptions
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
)
from . import models


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
        context['categories'] = models.ProductCategory.objects.all()
        return context


class ProductDetailView(DetailView):
    model = models.Product
    queryset = models.Product.objects.filter(
        status=models.StatusType.publish.value)
    template_name = "shop/product-detail.html"
