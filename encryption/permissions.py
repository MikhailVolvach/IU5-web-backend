from rest_framework import permissions
from encryption.models import EncryptionUser

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        print(bool(request.user and (request.user.role == EncryptionUser.Roles.USER)))
        return bool(request.user and (request.user.role == EncryptionUser.Roles.USER))

class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        # print(request.user)
        return bool(request.user and (request.user.role == EncryptionUser.Roles.MODERATOR))

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # print(request.user)
        return bool(request.user and (request.user.role == EncryptionUser.Roles.ADMIN))
