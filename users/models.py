from __future__ import unicode_literals
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
import os.path
import uuid

from utils import constant


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if 'master_email' in extra_fields and 'master_username' in extra_fields:
            master_email = self.normalize_email(extra_fields['master_email'])
            master_username = self.model.normalize_username(
                extra_fields['master_username'])
            del extra_fields['master_email']
            del extra_fields['master_username']
            user = self.model(master_email=master_email,
                              master_username=master_username, **extra_fields)
        else:
            if not email:
                raise ValueError('The given username must be set')
            email = self.normalize_email(email)
            username = self.model.normalize_username(username)
            user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, username, password, email=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)

def upload_path(instance, file_name):
    a = instance
    return '/'.join(['photo', 'local', file_name])

class PhotoModel(models.Model):
    photo = models.ImageField(blank=True, null=True, upload_to=upload_path)
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    class Meta:
        db_table = 'tbl_photo'
        ordering = ['id']

class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    photo = models.ForeignKey(PhotoModel, related_name='photo_user', on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(
        blank=True, null=True, max_length=20, unique=True)
    name = models.CharField(blank=True, null=True, max_length=30)
    description = models.CharField(blank=True, null=True, max_length=254, default="")
    phone = models.CharField(blank=True, null=True, max_length=20)
    slogan = models.CharField(blank=True, null=True,default="", max_length=50)
    position = models.SmallIntegerField(choices=constant.USER_POSITION_TYPE_OPTION,
                                        default=constant.USER_STUDENT, null=True, blank=True)
    owner_course = ArrayField(models.IntegerField(blank=True, null=True), blank=True, null=True)
    account_type = models.SmallIntegerField(choices=constant.ACCOUNT_TYPE,
                                            default=constant.ACCOUNT_TYPE_NORMAL, null=True, blank=True)
    objects = MyUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'tbl_user'
        ordering = ['id']

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.email

# class EmailBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:  # to allow authentication through phone number or any other field, modify the below statement
#             user = UserModel.objects.get(
#                 Q(username__iexact=username) | Q(email__iexact=username))
#         except UserModel.DoesNotExist:
#             UserModel().set_password(password)
#         except MultipleObjectsReturned:
#             return User.objects.filter(email=username).order_by('id').first()
#         else:
#             if user.check_password(password) and self.user_can_authenticate(user):
#                 return user

#     def get_user(self, user_id):
#         try:
#             user = UserModel.objects.get(pk=user_id)
#         except UserModel.DoesNotExist:
#             return None

#         return user if self.user_can_authenticate(user) else None
