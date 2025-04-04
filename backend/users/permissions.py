from rest_framework import permissions


class IsActive(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_active:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_active:
            return True
        return False
