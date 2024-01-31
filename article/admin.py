from django.contrib import admin
from .models import Articles, Tags, Category
from . import models


@admin.register(models.Articles)
class ArticlesAdmin(admin.ModelAdmin):
    autocomplete_fields = ["author"]
    prepopulated_fields = {"slug": ["title"]}
    list_display = ('title', 'status')
    list_filter = ('publish', 'status', 'category')
    search_fields = ('title', 'description')
    ordering = ['-publish']


admin.site.register(Category)
admin.site.register(Tags)