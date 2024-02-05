from django.contrib import admin
from .models import Variations, Attribute
from django.utils.safestring import mark_safe
from django.forms import Textarea
from django.db import models

# Register your models here.
class VariationsAdmin(admin.TabularInline):
    model = Variations
    extra = 1
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ('image_preview',)
    formfield_overrides = {
            models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':40})},
        }

    def image_preview(self, obj):
        # ex. the name of column is "image"
        if obj.image:
            return mark_safe('<img src="{0}" width="40" height="40" style="object-fit:contain" />'.format(obj.image.url))
        else:
            return '(No image)'

    image_preview.short_description = 'Preview'


@admin.register(Attribute)
class AttributesAdmin(admin.ModelAdmin):
    inlines = [VariationsAdmin]
    prepopulated_fields = {"slug": ["title"]}
    list_display = ('title', 'variations')

    def variations(self, obj):
        return ", ".join([k.title for k in obj.variation.all()])