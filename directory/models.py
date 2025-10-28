from django.db import models
from django.conf import settings


class SpamReport(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='spam_reports')
    phone = models.CharField(max_length=32, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('reporter', 'phone')]

# Create your models here.
