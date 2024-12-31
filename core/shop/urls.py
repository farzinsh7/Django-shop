from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("product/list", views.ProductListView.as_view(), name="product-list"),
]
