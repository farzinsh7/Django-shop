from django.contrib import admin
from .models import Product, Tags, Category, Gallery, Variant, GalleryVariations
from django.forms import Textarea, TextInput
from django.db import models
from .forms import ProductForm
from django.utils.safestring import mark_safe
import admin_thumbnails
import nested_admin

# from attribute.models import Attribute, Variations

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {"slug": ["title"]}


admin.site.register(Category, CategoryAdmin)


class TagsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {"slug": ["title"]}


admin.site.register(Tags, TagsAdmin)

@admin_thumbnails.thumbnail('image')
class GalleriesInline(nested_admin.NestedTabularInline):
    model = Gallery
    extra = 1
    readonly_fields = ('pk',)
    formfield_overrides = {
            models.CharField: {'widget': TextInput(attrs={'size':'30'})},
        }

@admin_thumbnails.thumbnail('image')
class GalleryVariationsInline(nested_admin.NestedTabularInline):
    model = GalleryVariations
    extra = 1


class VariantInline(nested_admin.NestedTabularInline):
    model = Variant
    # parent_model = Variant
    inlines = [GalleryVariationsInline]
    extra = 1
    show_change_link = True
    # formfield_overrides = {
    #         models.CharField: {'widget': TextInput(attrs={'size':'20'})},
    #     }


@admin.register(Product)
class ProductAdmin(nested_admin.NestedModelAdmin):
    form = ProductForm
    inlines = [GalleriesInline, VariantInline]
    prepopulated_fields = {"slug": ["title"]}
    list_display = ('thumbnail_tag', 'title')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        # ex. the name of column is "image"
        if obj.image:
            return mark_safe('<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.image.url))
        else:
            return '(No image)'
    
    image_preview.short_description = 'Preview'


