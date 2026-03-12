from rest_framework.permissions import BasePermission

from users.models import Agent, Admin

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class IsAgent(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and Agent.objects.filter(user=request.user, is_active=True).exists()
        )

class IsAdminOrSuperUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.is_staff or request.user.is_superuser)
        )


class IsOwnerOrAssignedAgent(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Ticket owner
        if obj.user == request.user:
            return True

        # Assigned agent
        if hasattr(obj, 'assigned_agent') and obj.assigned_agent:
            return obj.assigned_agent.user == request.user

        return False
