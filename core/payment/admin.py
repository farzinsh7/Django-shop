from django.contrib import admin
from . import models


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'authority_id',
                    'amount',
                    'response_code',
                    'status',
                    'created_at',
                    ]
