from rest_framework import serializers
from notifications.models import (
    NotificationEvent,
    NotificationChannel,
    NotificationTemplate,
    NotificationLog,
    WebhookEndpoint
)

# ==================================================
# Notification Event Serializer
# ==================================================
class NotificationEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationEvent
        fields = [
            "id",
            "code",
            "description",
            "is_active",
            "created_at"
        ]
        read_only_fields = ["id", "created_at"]


# ==================================================
# Notification Channel Serializer
# ==================================================
class NotificationChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationChannel
        fields = [
            "id",
            "name",
            "is_active",
            "created_at"
        ]
        read_only_fields = ["id", "created_at"]


# ==================================================
# Notification Template Serializer
# ==================================================
class NotificationTemplateSerializer(serializers.ModelSerializer):
    event_code = serializers.CharField(source="event.code", read_only=True)
    channel_name = serializers.CharField(source="channel.name", read_only=True)

    class Meta:
        model = NotificationTemplate
        fields = [
            "id",
            "event",
            "event_code",
            "channel",
            "channel_name",
            "subject_template",
            "body_template",
            "is_active",
            "created_at"
        ]
        read_only_fields = ["id", "created_at"]


# ==================================================
# Notification Log Serializer (READ-ONLY)
# ==================================================
class NotificationLogSerializer(serializers.ModelSerializer):
    event_code = serializers.CharField(source="event.code", read_only=True)
    channel_name = serializers.CharField(source="channel.name", read_only=True)

    class Meta:
        model = NotificationLog
        fields = [
            "id",
            "event_code",
            "channel_name",
            "recipient_address",
            "status",
            "error_message",
            "created_at",
            "sent_at"
        ]
        read_only_fields = fields


# ==================================================
# Webhook Endpoint Serializer
# ==================================================
class WebhookEndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEndpoint
        fields = [
            "id",
            "name",
            "url",
            "secret_token",
            "is_active",
            "created_at"
        ]
        read_only_fields = ["id", "created_at"]
