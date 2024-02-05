from django.contrib import admin
from .models import Variations, Attribute

# Register your models here.
class VariationsAdmin(admin.TabularInline):
    model = Variations
    extra = 1
    prepopulated_fields = {"slug": ["title"]}


@admin.register(Attribute)
class AttributesAdmin(admin.ModelAdmin):
    inlines = [VariationsAdmin]
    prepopulated_fields = {"slug": ["title"]}