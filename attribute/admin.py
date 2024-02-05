from django.contrib import admin
from .models import Variations, Attribute
from django.utils.safestring import mark_safe
from django.forms import Textarea, TextInput
from django.db import models
from django.utils.html import format_html

# Register your models here.
class VariationsAdmin(admin.TabularInline):
    model = Variations
    extra = 1
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ('image_preview',)
    formfield_overrides = {
            models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':40})},
            models.CharField: {'widget': TextInput(attrs={'size':'20'})},
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
    list_display = ('title', 'labels')

    
    def labels(self, obj):
        images_html = [k.label() for k in obj.variation.all()]
        return format_html(" ".join(images_html))
