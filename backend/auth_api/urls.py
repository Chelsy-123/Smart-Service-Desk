from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, AgentCreateView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('agents/create/', AgentCreateView.as_view()),
]

# api endpoints:
# /api/auth/register/
# /api/auth/login/
# /api/auth/agents/create/