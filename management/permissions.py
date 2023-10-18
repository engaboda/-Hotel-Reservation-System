from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    message = 'not-allowed'

    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_staff
