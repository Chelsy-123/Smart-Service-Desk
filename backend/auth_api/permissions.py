from rest_framework.permissions import BasePermission
from users.models import Admin

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return Admin.objects.filter(user=request.user).exists()
