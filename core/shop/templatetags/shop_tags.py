from django import template
from shop import models

register = template.Library()


@register.inclusion_tag("includes/latest-products.html")
def show_latest_products():
    latest_products = models.Product.objects.prefetch_related("category").filter(
        status=models.StatusType.publish.value).order_by("-created_at")[:8]
    return {"latest_products": latest_products}
