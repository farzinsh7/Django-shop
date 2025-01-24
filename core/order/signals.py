from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, OrderStatus
from shop.models import Product


@receiver(post_save, sender=Order)
def update_product_stock(sender, instance, **kwargs):
    if instance.status == OrderStatus.processing.value:
        for item in instance.order_items.all():
            product = item.product

            # Ensure sufficient stock is available
            if product.stock < item.quantity:
                raise ValueError(
                    f"Insufficient stock for product '{product.title}'. Available: {product.stock}, Required: {item.quantity}"
                )

            # Subtract the quantity from the product's stock
            product.stock -= item.quantity
            product.save()
