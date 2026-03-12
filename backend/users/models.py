from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agent_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.agent_name


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class UserNotificationPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(
        "notifications.NotificationChannel",
        on_delete=models.CASCADE
    )
    is_enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'channel')

    def __str__(self):
        return f"{self.user.username} - {self.channel.name}"
