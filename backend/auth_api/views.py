from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import RegisterSerializer, AgentCreateSerializer, AgentResponseSerializer
from common.permissions import IsAdminOrSuperUser  # you already have this

User = get_user_model()


# -------------------------
# REGISTER (NORMAL USERS)
# -------------------------
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# -------------------------
# LOGIN (USER / AGENT / ADMIN)
# -------------------------
class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        token['groups'] = list(user.groups.values_list('name', flat=True))
        return token


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


# -------------------------
# ADMIN → CREATE AGENT
# -------------------------
class AgentCreateView(generics.CreateAPIView):
    serializer_class = AgentCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        agent = serializer.save()

        response_serializer = AgentResponseSerializer(agent)
        return Response(response_serializer.data, status=201)
