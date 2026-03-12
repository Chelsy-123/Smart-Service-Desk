from rest_framework.routers import DefaultRouter
from notifications.views import (
    UserNotificationPreferenceViewSet,
    NotificationLogViewSet
)

router = DefaultRouter()
router.register(r'preferences', UserNotificationPreferenceViewSet, basename='UserNotificationPreference')
router.register(r'logs', NotificationLogViewSet, basename='NotificationLog')

urlpatterns = router.urls
# api endpoints:
# /api/notifications/preferences/
# /api/notifications/logs/