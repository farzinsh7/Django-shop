from django.contrib import admin
from .models import Variations, Attribute

# Register your models here.
class VariationsAdmin(admin.TabularInline):
    model = Variations
    extra = 1


@admin.register(Attribute)
class AttributesAdmin(admin.ModelAdmin):
    inlines = [VariationsAdmin]