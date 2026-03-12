from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from notifications.models import  NotificationLog
from notifications.serializers import (
    NotificationLogSerializer
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser 

from users.models import UserNotificationPreference
from users.serializers import UserNotificationPreferenceSerializer

class UserNotificationPreferenceViewSet(viewsets.ModelViewSet):
    serializer_class = UserNotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserNotificationPreference.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



# notifications/views.py

from rest_framework import viewsets, permissions
from notifications.models import NotificationLog
from notifications.serializers import NotificationLogSerializer


class NotificationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    - Users: see their own notifications
    - Admins: see all notifications
    """
    serializer_class = NotificationLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Admin can see all notifications
        if user.is_superuser:
            return NotificationLog.objects.all().order_by('-created_at')

        # Normal user sees only their notifications
        return NotificationLog.objects.filter(
            recipient_user=user
        ).order_by('-created_at')

