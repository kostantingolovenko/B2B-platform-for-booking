from rest_framework import permissions

from invoice.models import Invoice


class IsAdminAndInOrganization(permissions.BasePermission):
    def has_permission(self, request, view):
            return bool(request.user.is_authenticated and request.user.organization and request.user.is_staff)