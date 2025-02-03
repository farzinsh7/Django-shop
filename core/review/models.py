from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from shop.models import Product
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ReviewStatusType(models.IntegerChoices):
    pending = 1, _("در انتظار تایید")
    accepted = 2, _("تایید شده")
    rejected = 3, _("رد شده")


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField()
    rate = models.IntegerField(default=5, validators=[
                               MinValueValidator(0), MaxValueValidator(5)])
    status = models.IntegerField(
        choices=ReviewStatusType.choices, default=ReviewStatusType.pending.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by: {self.user} for Product: {self.product}"
