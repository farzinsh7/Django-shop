from django.urls import path
from .views import ArticlesListView, ArticleDetailView

app_name = "article"
urlpatterns = [
    path('articles/', NewsListView.as_view(), name="list_view"),
    path('articles/<slug:slug>', NewsDetailView.as_view(), name='detail_view'),
]