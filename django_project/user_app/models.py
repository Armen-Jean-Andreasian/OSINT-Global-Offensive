from django.contrib.auth.models import AbstractUser
from django.db import models
import hashlib
import os
import uuid


class UserModel(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, blank=False, null=False)
    password = models.CharField(max_length=255, blank=False, null=False)
    salt = models.CharField(max_length=255, blank=False, null=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # This will prevent the clash with the default 'user_set'
        blank=True
    )

    # Override the default `user_permissions` field to avoid the clash
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_permission_set',  # This will prevent the clash with the default 'user_set'
        blank=True
    )

    def set_password(self, password: str, overwrite=False):
        if not self.password or overwrite:
            salt = os.urandom(16).hex()
            self.salt = salt

            self.password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        else:
            raise NotImplementedError("If you try to overwrite password, set it to True as param")

    def check_password(self, password: str) -> bool:
        return self.password == hashlib.sha256((password + self.salt).encode('utf-8')).hexdigest()
