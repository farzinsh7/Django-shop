from django.db import models


class ContactUsModel(models.Model):
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    phone = models.CharField(max_length=11)
    email = models.EmailField(null=True)
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
