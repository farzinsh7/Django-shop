# Generated by Django 5.0.1 on 2024-02-05 12:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attribute', '0005_remove_attribute_product'),
        ('product', '0025_remove_variant_variations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variant',
            name='attribute',
        ),
        migrations.AddField(
            model_name='variant',
            name='variations',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='attribute.variations'),
        ),
    ]
