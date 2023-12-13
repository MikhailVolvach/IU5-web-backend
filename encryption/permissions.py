from rest_framework import permissions
from encryption.models import EncryptionUser

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # print(request.user)
        # print(bool(request.user and (request.user.role == EncryptionUser.Roles.USER)))
        return bool(request.user and not request.user.is_staff)

class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        # print(request.user)
        return bool(request.user and request.user.is_staff)

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # print(request.user)
        return bool(request.user and request.user.is_superuser)
