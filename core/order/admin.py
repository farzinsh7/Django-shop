from django.contrib import admin
from . import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'user',
                    'status',
                    'coupon',
                    'total_price',
                    'created_at',
                    ]
    readonly_fields = ('coupon_at_order',)


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'order',
                    'product',
                    'quantity',
                    'price',
                    'created_at',
                    ]


@admin.register(models.Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'code',
                    'description',
                    'discount_percent',
                    'max_limit_usage',
                    'used_by_count',
                    'expiration_date',
                    'created_at',
                    ]

    def used_by_count(self, obj):
        return obj.used_by.all().count()


@admin.register(models.UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'user',
                    'state',
                    'city',
                    'zip_code',
                    'created_at',
                    ]
