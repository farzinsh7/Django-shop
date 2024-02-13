from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.html import format_html

# Create your models here.
class Color(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='variations/color', null=True, blank=True)


    def __str__(self):
        return self.title

    def label(self):
        if self.image:
            return format_html("<img width=40 height=40 style='border-radius: 5px;' src='{}'>".format(self.image.url))
        else:
            return format_html("{}, ".format(self.title))
    
    label.short_description = "label"