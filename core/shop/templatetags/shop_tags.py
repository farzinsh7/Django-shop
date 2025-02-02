from django import template
from shop import models

register = template.Library()


@register.inclusion_tag("includes/latest-products.html", takes_context=True)
def show_latest_products(context):
    request = context.get("request")
    latest_products = models.Product.objects.prefetch_related("category").filter(
        status=models.StatusType.publish.value).order_by("-created_at")[:8]
    if request.user.is_authenticated:
        wishlist_products = models.WishlistProducts.objects.filter(
            user=request.user
        ).values_list('product__id', flat=True)
    else:
        wishlist_products = []
    return {"latest_products": latest_products, "request": request, "wishlist_products": wishlist_products}


@register.inclusion_tag("includes/similar-products.html", takes_context=True)
def show_similar_products(context, product):
    request = context.get("request")
    product_categories = product.category.all()
    similar_products = models.Product.objects.prefetch_related("category").filter(
        status=models.StatusType.publish.value, category__in=product_categories).exclude(id=product.id).distinct().order_by("-created_at")[:4]
    if request.user.is_authenticated:
        wishlist_products = models.WishlistProducts.objects.filter(
            user=request.user
        ).values_list('product__id', flat=True)
    else:
        wishlist_products = []
    return {"similar_products": similar_products, "request": request, "wishlist_products": wishlist_products}
