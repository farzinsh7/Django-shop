import random
from django.core.management.base import BaseCommand
from faker import Faker
from shop.models import ProductCategory
from django.utils.text import slugify

fake = Faker(locale="fa-IR")


class Command(BaseCommand):
    help = "Generate 10 fake ProductCategory entries"

    def handle(self, *args, **kwargs):
        for _ in range(10):
            title = fake.word().capitalize()
            ProductCategory.objects.get_or_create(
                title=title,
                slug=slugify(title, allow_unicode=True),
                image=f"product/category/{fake.file_name(extension='jpg')}",
                description=fake.text(max_nb_chars=200)
            )
        self.stdout.write(self.style.SUCCESS(
            "Successfully created 10 fake ProductCategory entries."))
