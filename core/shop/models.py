from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusType(models.IntegerChoices):
    draft = 1, _("draft")
    publish = 2, _("publish")


class ProductCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)
    image = models.ImageField(upload_to="product/category/")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT)
    category = models.ManyToManyField(ProductCategory)
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)
    image = models.ImageField(upload_to="product/img")
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    status = models.IntegerField(
        choices=StatusType.choices, default=StatusType.draft.value)
    sku = models.CharField(unique=True)
    price = models.DecimalField(default=0, max_digits=15, decimal_places=0)
    discount_percent = models.IntegerField(0)
    created_at = models.DateTimeField(auto_created=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product/img")
    created_at = models.DateTimeField(auto_created=True)
    updated_date = models.DateTimeField(auto_now=True)
