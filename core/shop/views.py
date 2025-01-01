from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
)
from . import models


class ProductGridView(ListView):
    template_name = "shop/product-grid.html"
    paginate_by = 3

    def get_queryset(self):
        queryset = models.Product.objects.prefetch_related("category").filter(
            status=models.StatusType.publish.value)
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        elif category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
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
