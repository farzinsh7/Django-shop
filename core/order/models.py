from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="آدرس پستی")
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class OrderStatus(models.IntegerChoices):
    pending = 1, _("در حال انتظار")
    processing = 2, _("در حال پردازش")
    shipped = 3, _("در حال ارسال")
    deliverd = 4, _("تحویل داده شده")
    cancelled = 5, _("لغو شده")
    refund = 6, _("عودت داده شده")


class Coupon(models.Model):
    code = models.CharField(max_length=255)
    description = models.TextField()
    discount_percent = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_limit_usage = models.PositiveIntegerField(default=10)
    used_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="coupon_users", blank=True)
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
    coupon_at_order = models.IntegerField(default=0)
    total_price = models.DecimalField(
        default=0, max_digits=15, decimal_places=0)

    # order address information
    title = models.CharField(max_length=255, default="آدرس پستی")
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)

    payment = models.ForeignKey(
        'payment.Payment', on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.id}"

    def calculate_total_price(self):
        return sum(item.price * item.quantity for item in self.order_items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name="order_items")
    product = models.ForeignKey('shop.Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=15, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.title} - {self.order.id}"
