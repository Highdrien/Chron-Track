import uuid
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for Chron Track.

    Inherits from AbstractUser which already provides:
    username, first_name, last_name, is_staff, is_active, date_joined.
    """

    id: uuid.UUID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    email: str = models.EmailField(unique=True)

    created_at: datetime = models.DateTimeField(auto_now_add=True)
    updated_at: datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email
