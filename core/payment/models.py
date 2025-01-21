from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentStatus(models.IntegerChoices):
    pending = 1, _("pending")
    success = 2, _("success")
    failed = 3, _("failed")


# Create your models here.
class Payment(models.Model):
    authority_id = models.CharField(max_length=255)
    ref_id = models.BigIntegerField(null=True, blank=True)
    amount = models.DecimalField(default=0, max_digits=15, decimal_places=0)
    response_json = models.JSONField(default=dict)
    response_code = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(
        choices=PaymentStatus.choices, default=PaymentStatus.pending.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
