# Generated by Django 5.0.1 on 2024-02-05 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_product_attributes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvariation',
            name='variation',
        ),
    ]
