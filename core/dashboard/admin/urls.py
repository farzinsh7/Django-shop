from django.urls import path
from . import views

app_name = "admin"

urlpatterns = [
    path("home/", views.AdminDashboardHomeView.as_view(), name="home"),
    path("security/edit/", views.AdminSecurityEditView.as_view(),
         name="security-edit"),
    path("profile/edit/", views.AdminProfileEditView.as_view(), name="profile-edit"),
    path("profile/edit/image/", views.AdminProfileImageEditView.as_view(),
         name="profile-image-edit"),
    path("product/list/", views.AdminProductListView.as_view(), name="product-list"),
    path("product/<int:pk>/edit/",
         views.AdminProductEditView.as_view(), name="product-edit"),
    path("product/create/",
         views.AdminProductCreateView.as_view(), name="product-create"),
    path("product/<int:pk>/delete/",
         views.AdminProductDeleteView.as_view(), name="product-delete"),
]
