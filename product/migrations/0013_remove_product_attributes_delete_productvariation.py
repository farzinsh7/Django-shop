# Generated by Django 5.0.1 on 2024-02-05 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_remove_productvariation_variation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='attributes',
        ),
        migrations.DeleteModel(
            name='ProductVariation',
        ),
    ]
