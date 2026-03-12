from django.contrib import admin
from .models import NotificationChannel, NotificationEvent, NotificationTemplate, NotificationLog, WebhookEndpoint
# Register your models here.
admin.site.register(NotificationChannel)
admin.site.register(NotificationEvent)
admin.site.register(NotificationTemplate)
admin.site.register(NotificationLog)
admin.site.register(WebhookEndpoint)