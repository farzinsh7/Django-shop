from django.urls import path
from .views import ProductListView, ProductDetailView


app_name = "product"
urlpatterns = [
    path('shop/', ProductListView.as_view(), name="list_view"),
    path('shop/<slug:slug>', ProductDetailView.as_view(), name='detail_view'),
]