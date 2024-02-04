from django.urls import path
from .views import my_view


app_name = "home"
urlpatterns = [
    path('', my_view, name="page"),
]