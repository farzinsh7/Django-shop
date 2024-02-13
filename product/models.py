from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.html import format_html
from attribute.models import Color

# Create your models here.
class ProductsManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class Category(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=200, unique=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Tags(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=200, unique=True)
    status = models.BooleanField(default=True)


    def __str__(self):
        return self.title



class Product(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Publish')
    )
    VARIATIONS = (
        ('c', 'Color'),
        ('s', 'Size')
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    description = RichTextUploadingField(null=True)
    short_description = RichTextUploadingField(null=True)
    price = models.IntegerField()
    sku = models.CharField(max_length=200, null=True, blank=True, unique=True)
    dimenstions = models.CharField(max_length=200, null=True, blank=True)
    category = models.ManyToManyField(Category, related_name='category')
    tag = models.ManyToManyField(Tags, related_name='tag')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, null=True)
    variation = models.CharField(max_length=1, choices=VARIATIONS, null=True)
    image = models.ImageField(upload_to='shop/image', null=True, blank=True)
    # tax_class = pass
    # shiping_class = pass
    # related_product = pass


    def __str__(self):
        return self.title
    
    def thumbnail_tag(self):
        return format_html(
            "<img width=200 height=200 style='border-radius: 5px;' src='{}'>".format(self.image.url))

    thumbnail_tag.short_description = "Thumbnail"

    objects = ProductsManager()


class Gallery(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='shop/gallery', null=True, blank=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, related_name='gallery')


    def __str__(self):
        return self.title
