from django.shortcuts import render
from django.views.generic import TemplateView


class ProductListView(TemplateView):
    template_name = "shop/product-list.html"
