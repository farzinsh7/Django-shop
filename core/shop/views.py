from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
)
from . import models


class ProductGridView(ListView):
    queryset = models.Product.objects.filter(
        status=models.StatusType.publish.value)
    template_name = "shop/product-grid.html"
