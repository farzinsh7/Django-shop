from django.urls import path
from .. import views


urlpatterns = [
    path("orders/list/", views.CustomerOrdersListView.as_view(), name="orders-list"),
    path("orders/<int:pk>/detail/", views.CustomerOrderDetailView.as_view(),
         name="order-detail"),
    path("orders/<int:pk>/invoice/", views.CustomerOrderInvoiceView.as_view(),
         name="order-invoice"),
]
