from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review, ReviewStatusType
from django.db.models import Avg


@receiver(post_save, sender=Review)
def calculate_avg_rate_review(sender, **kwargs):
    if kwargs['instance'].status == ReviewStatusType.accepted.value:
        product = kwargs['instance'].product
        average_rating = Review.objects.filter(
            product=product, status=ReviewStatusType.accepted).aggregate(Avg('rate'))['rate__avg']
        product.avg_rate = round(average_rating, 1)
        product.save()
