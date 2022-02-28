from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models


# BaseManager :
class BaseManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    # define method for access all queryset
    def get_archive(self):
        return super().get_queryset()

    # define method for access all active query
    def get_active_list(self):
        return super().get_queryset().filter(is_deleted=False, is_active=True)

    # define deleted item for easy access data
    def get_deleted_list(self):
        return super().get_queryset().filter(is_deleted=True)

    # define deactivate item
    def get_deactivate_list(self):
        return self.get_queryset().filter(is_active=False)


class MyUserManager(UserManager):
    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        username = extra_fields['phone']
        return super().create_superuser(username, email, password, **extra_fields)

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        username = extra_fields['phone']
        return super().create_user(username, email, password, **extra_fields)
