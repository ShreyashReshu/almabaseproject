from django.db import models
from django.conf import settings


class Contact(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=32, db_index=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('owner', 'phone')]

# Create your models here.
