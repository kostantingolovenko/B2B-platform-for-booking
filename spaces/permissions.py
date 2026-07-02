from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.organization)

    def has_object_permission(self, request, view, obj):
        if obj.get_organization() != request.user.organization:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff
