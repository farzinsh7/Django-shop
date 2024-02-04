from django.urls import path
from .views import ArticlesListView, ArticleDetailView

app_name = "article"
urlpatterns = [
    # path('articles/', ArticlesListView.as_view(), name="list_view"),
    # path('articles/<slug:slug>', ArticleDetailView.as_view(), name='detail_view'),
]