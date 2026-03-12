from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from common.permissions import IsAdminOrSuperUser
from users.models import User, Agent
from users.serializers import UserSerializer, AgentSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

from users.serializers import ChangePasswordSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    Logged-in users can view their own profile
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    def perform_update(self, serializer):
        # Prevent privilege escalation
        serializer.save(
            is_superuser=self.request.user.is_superuser,
            is_staff=self.request.user.is_staff
        )

class AgentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Admins can view agent list
    """
    serializer_class = AgentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperUser]

    def get_queryset(self):
        return Agent.objects.filter(is_active=True)
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        # Check old password
        if not user.check_password(serializer.validated_data["old_password"]):
            return Response(
                {"detail": "Old password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Set new password
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"detail": "Password changed successfully"},
            status=status.HTTP_200_OK
        )
