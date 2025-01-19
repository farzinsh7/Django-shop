from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class OrderStatus(models.IntegerChoices):
    pending = 1, _("pending")
    processing = 2, _("processing")
    shipped = 3, _("shipped")
    deliverd = 4, _("deliverd")
    cancelled = 5, _("cancelled")
    refund = 6, _("refund")


class Coupon(models.Model):
    code = models.CharField(max_length=255)
    description = models.TextField()
    discount_percent = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_limit_usage = models.PositiveIntegerField(default=10)
    used_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="coupon_users")
    expiration_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT)
    status = models.IntegerField(
        choices=OrderStatus.choices, default=OrderStatus.pending.value)
    coupon = models.ForeignKey(
        Coupon, on_delete=models.PROTECT, null=True, blank=True)
    total_price = models.DecimalField(
        default=0, max_digits=15, decimal_places=0)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey('shop.Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=15, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
