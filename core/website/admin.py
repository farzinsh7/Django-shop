from django.contrib import admin
from . import models


@admin.register(models.ContactUsModel)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'email', 'description']
