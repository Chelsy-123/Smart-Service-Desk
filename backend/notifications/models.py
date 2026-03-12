from django.db import models
from django.conf import settings

# ==================================================
# NOTIFICATION MODELS
# ==================================================

class NotificationEvent(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


class NotificationChannel(models.Model):
    name = models.CharField(max_length=50, unique=True)  # EMAIL, WEBHOOK
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class NotificationTemplate(models.Model):
    event = models.ForeignKey(NotificationEvent, on_delete=models.CASCADE)
    channel = models.ForeignKey(NotificationChannel, on_delete=models.CASCADE)

    subject_template = models.CharField(max_length=255, blank=True, null=True)
    body_template = models.TextField()

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.code} - {self.channel.name}"


class NotificationLog(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('FAILED', 'Failed'),
    ]

    event = models.ForeignKey(NotificationEvent, on_delete=models.CASCADE)
    channel = models.ForeignKey(NotificationChannel, on_delete=models.CASCADE)

    recipient_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    recipient_address = models.CharField(max_length=255)

    payload = models.JSONField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    error_message = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Notification {self.id} - {self.status}"


class WebhookEndpoint(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    secret_token = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
