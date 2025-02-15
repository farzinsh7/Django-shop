# Generated by Django 4.2.17 on 2025-01-24 13:31

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='short_description',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
    ]
