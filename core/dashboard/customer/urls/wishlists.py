from django.urls import path
from .. import views


urlpatterns = [
    path("wishlist/list/", views.CustomerWishlistListView.as_view(),
         name="wishlist-list"),

]
