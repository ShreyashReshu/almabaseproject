from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=32, unique=True, db_index=True)
    email = models.EmailField(blank=True, null=True, unique=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    def __str__(self) -> str:
        return f"{self.name} ({self.phone})"

# Create your models here.
