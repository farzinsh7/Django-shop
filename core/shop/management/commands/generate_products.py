import random
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from faker import Faker
from shop.models import Product, ProductCategory, StatusType
from django.contrib.auth import get_user_model
from django.utils.text import slugify

fake = Faker()


class Command(BaseCommand):
    help = "Generate 100 fake Product entries"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        commands_dir = os.path.dirname(__file__)
        images_dir = os.path.join(commands_dir, "images")
        images_list = [
            os.path.join("images", filename)
            for filename in os.listdir(images_dir)
            if filename.endswith((".jpg", ".png", ".jpeg"))
        ]

        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.ERROR(
                "No users found. Create at least one user first."
            ))
            return

        categories = ProductCategory.objects.all()
        if not categories.exists():
            self.stdout.write(self.style.ERROR(
                "No categories found. Run generate_categories first."
            ))
            return

        for i in range(100):
            user = random.choice(users)  # Randomly select a user
            title = fake.sentence(nb_words=3).rstrip(".")
            product = Product.objects.create(
                user=user,
                title=title,
                slug=slugify(title, allow_unicode=True),
                image=random.choice(images_list),
                description=fake.text(max_nb_chars=200),
                stock=random.randint(0, 10),
                status=random.choice(StatusType.choices)[0],
                sku=fake.unique.ean(length=13),
                price=round(random.uniform(2000000, 90000000)),
                discount_percent=random.randint(0, 50),
            )

            # Assign random categories to the product
            product.category.set(
                random.sample(list(categories), k=random.randint(1, 3))
            )

            if i % 10 == 0:
                self.stdout.write(f"{i} products created...")

        self.stdout.write(self.style.SUCCESS(
            "Successfully created 100 fake Product entries."
        ))
