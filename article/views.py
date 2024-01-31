from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Articles

# Create your views here.
class ArticlesListView(ListView):
    queryset = Articles.objects.published()
    model = Articles
    template_name = 'articles_list.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest'] = Articles.objects.published()[:5]
        return context

class ArticleDetailView(DetailView):
    model = Articles
    context_object_name = 'articles'
    queryset = Articles.objects.published()
    template_name = 'articles_detail.html'