from django.db.models.signals import post_save
from django.dispatch import receiver
from shop.models import Product
from .models import Review


@receiver(post_save, sender=Review)
def calculate_avg_rate_review(sender, **kwargs):
    pass
