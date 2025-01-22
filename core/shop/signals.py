from django.dispatch import receiver
from django.db.models.signals import post_save
from order.models import OrderItem


@receiver(post_save, sender=OrderItem)
def subtract_product_stock(sender, instance, created, **kwargs):
    if created:  # Ensure this runs only when a new OrderItem is created
        product = instance.product
        if product.stock >= instance.quantity:
            product.stock -= instance.quantity
            product.save()
        else:
            raise ValueError(f"موجودی محصول {product.title} کم می باشد.")
