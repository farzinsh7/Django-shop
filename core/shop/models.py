from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
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
    category = models.ManyToManyField(ProductCategory, related_name="category")
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)
    image = models.ImageField(upload_to="product/img")
    description = models.TextField()
    short_description = models.TextField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    status = models.IntegerField(
        choices=StatusType.choices, default=StatusType.draft.value)
    sku = models.CharField(unique=True)
    price = models.DecimalField(default=0, max_digits=15, decimal_places=0)
    discount_percent = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_price(self):
        discount_amount = int(self.price) * (self.discount_percent / 100)
        final_amount = int(self.price) - discount_amount
        return int(final_amount)

    def get_show_price(self):
        discount_amount = int(self.price) * (self.discount_percent / 100)
        final_amount = int(self.price) - discount_amount
        return "{:,}".format(int(final_amount))

    class Meta:
        ordering = ["-created_at"]


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product/img")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
