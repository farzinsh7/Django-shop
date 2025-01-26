from django.urls import path, include
from . import views

app_name = "customer"

urlpatterns = [
    path("home/", views.CustomerDashboardHomeView.as_view(), name="home"),
    path("security/edit/", views.CustomerSecurityEditView.as_view(),
         name="security-edit"),
    path("profile/edit/", views.CustomerProfileEditView.as_view(), name="profile-edit"),
    path("profile/edit/image/",
         views.CustomerProfileImageEditView.as_view(), name="profile-image-edit"),
    path("address/create/", views.CustomerAddressCreateView.as_view(),
         name="address-create"),
    path("address/list/", views.CustomerAddressListView.as_view(), name="address-list"),
    path("address/<int:pk>/edit/",
         views.CustomerAddressEditView.as_view(), name="address-edit"),
    path("address/<int:pk>/delete/",
         views.CustomerAddressDeleteView.as_view(), name="address-delete"),
    path("orders/list/", views.CustomerOrdersListView.as_view(), name="orders-list"),
]
