from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group as AuthGroup, Permission as AuthPermission

class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('У пользователя должно быть имя')

        user = self.model(
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_moderator(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('У модератора должно быть имя')

        extra_fields.setdefault('role', 2)

        return self.create_user(username, password, **extra_fields)

    def create_admin(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('У администратора должно быть имя')

        extra_fields.setdefault('role', 3)

        return self.create_user(username, password, **extra_fields)
#
# class EncryptionUser(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=30, unique=True, verbose_name='Имя пользователя')
#     password = models.CharField(max_length=50, verbose_name='Пароль')
#     # is_staff = models.BooleanField(default=False, verbose_name='Является ли пользователь менеджером?')
#     # is_admin = models.BooleanField(default=False, verbose_name='Является ли пользователь администратором?')
#     class UserRoles(models.IntegerChoices):
#         USER = 1
#         MODERATOR = 2
#         ADMIN = 3
#
#     role = models.IntegerField(choices=UserRoles.choices, default=UserRoles.USER, verbose_name='Кем является пользователь?')
#
#     USERNAME_FIELD = 'username'
#
#     objects = MyUserManager()
#
#     def __str__(self):
#         return self.username
#
#


# class NewUserManager(BaseUserManager):
#     def create_user(self, username, password=None, **extra_fields):
#         if not username:
#             raise ValueError('User must have an username')
#
#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self.db)
#         return user


class EncryptionUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True, verbose_name="Имя пользователя")
    # password = models.CharField(max_length=50, verbose_name="Пароль")

    class Roles(models.IntegerChoices):
        USER = 1
        MODERATOR = 2
        ADMIN = 3

    role = models.IntegerField(choices=Roles.choices, default=Roles.USER, verbose_name="Роль пользователя", blank=True)

    USERNAME_FIELD = 'username'

    objects = MyUserManager()