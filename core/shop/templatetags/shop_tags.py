from django import template
from shop import models

register = template.Library()


@register.inclusion_tag("includes/latest-products.html")
def show_latest_products():
    latest_products = models.Product.objects.prefetch_related("category").filter(
        status=models.StatusType.publish.value).order_by("-created_at")[:8]
    return {"latest_products": latest_products}


@register.inclusion_tag("includes/similar-products.html")
def show_similar_products(product):
    product_categories = product.category.all()
    similar_products = models.Product.objects.prefetch_related("category").filter(
        status=models.StatusType.publish.value, category__in=product_categories).exclude(id=product.id).distinct().order_by("-created_at")[:4]
    return {"similar_products": similar_products}
