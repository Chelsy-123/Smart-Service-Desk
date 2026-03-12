from django.urls import path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, AgentViewSet, ChangePasswordView

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'agents', AgentViewSet, basename='agent')

urlpatterns = [
    # APIView → must be added manually
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]

# Router URLs MUST be appended, not assigned
urlpatterns += router.urls


# api endpoints:
#/api/users/user/
# /api/users/agents/