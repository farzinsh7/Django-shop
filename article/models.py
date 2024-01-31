from django.db import models
from django.utils import timezone
from account.models import User
from ckeditor_uploader.fields import RichTextUploadingField



class NewsManager(models.Manager):
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


class Articles(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Publish')
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles')
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ManyToManyField(Category, related_name='articles')
    tags = models.ManyToManyField(Tags, related_name='articles', blank=True)
    description = RichTextUploadingField()
    image = models.ImageField(upload_to='articles')
    thumbnail = models.ImageField(upload_to='articles/thumb', null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    keywords = models.CharField(max_length=300, null=True)
    seo_description = models.TextField(null=True)


    def __str__(self):
        return self.title

    objects = NewsManager()