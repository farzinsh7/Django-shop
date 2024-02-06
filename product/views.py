from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product

# Create your views here.
class ProductListView(ListView):
    queryset = Product.objects.published()
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'product'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest'] = Product.objects.published()[:5]
        return context


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    queryset = Product.objects.published()
    template_name = 'product_detail.html'
