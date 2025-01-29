from django.urls import path
from .. import views


urlpatterns = [
    path("wishlist/list/", views.CustomerWishlistListView.as_view(),
         name="wishlist-list"),
    path('wishlist/add/', views.AddToWishlistView.as_view(), name='add_to_wishlist'),
    path("wishlist/<int:pk>/delete/",
         views.CustomerWishlistDeleteView.as_view(), name="wishlist-delete"),
]
