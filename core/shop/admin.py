from django.contrib import admin
from django.utils.html import format_html, urlencode
from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'stock',
                    'price', 'discount_percent', 'get_price', 'created_at']


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at']
