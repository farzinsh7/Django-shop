from django.urls import path
from .. import views


urlpatterns = [
    path("order/list/", views.AdminOrderListView.as_view(), name="orders-list"),
    path("order/<int:pk>/edit/",
         views.AdminOrderEditView.as_view(), name="order-edit"),
    path("order/<int:pk>/delete/",
         views.AdminOrderDeleteView.as_view(), name="order-delete"),
]
