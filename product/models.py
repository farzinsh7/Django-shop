from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
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
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    description = RichTextUploadingField(null=True)
    short_description = RichTextUploadingField(null=True)
    image = models.ImageField(upload_to='shop/image', null=True, blank=True)
    regular_price = models.IntegerField()
    sale_price = models.IntegerField(null=True, blank=True)
    sku = models.IntegerField(unique=True)
    dimenstions = models.IntegerField(null=True, blank=True)
    stock_quantity = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, related_name='category')
    tag = models.ManyToManyField(Tags, related_name='tag')
    # tax_class = pass
    # shiping_class = pass
    # related_product = pass
    # variation = pass


    def __str__(self):
        return self.title
    

class Gallery(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='shop/gallery', null=True, blank=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, related_name='gallery')


    def __str__(self):
        return self.title
    



