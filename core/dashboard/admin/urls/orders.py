from django.urls import path
from .. import views


urlpatterns = [
    path("order/list/", views.AdminOrderListView.as_view(), name="orders-list"),
    path("order/<int:pk>/edit/",
         views.AdminOrderEditView.as_view(), name="order-edit"),
    path("orders/<int:pk>/invoice/", views.AdminOrderInvoiceView.as_view(),
         name="order-invoice"),
]
