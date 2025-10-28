from django.db import models
from django.conf import settings


class Interaction(models.Model):
    TYPE_CALL = 'call'
    TYPE_MESSAGE = 'message'
    TYPE_SPAM = 'spam'
    TYPE_CHOICES = [
        (TYPE_CALL, 'Call'),
        (TYPE_MESSAGE, 'Message'),
        (TYPE_SPAM, 'Spam'),
    ]

    initiator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interactions_initiated')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interactions_received', null=True, blank=True)
    phone = models.CharField(max_length=32, db_index=True, blank=True)
    type = models.CharField(max_length=16, choices=TYPE_CHOICES)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['initiator', 'created_at']),
            models.Index(fields=['receiver', 'created_at']),
            models.Index(fields=['type', 'created_at']),
        ]

# Create your models here.
