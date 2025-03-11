from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    is_verified = models.BooleanField(default=False)  # Email verification status

    # Fix conflicts with AbstractUser
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",  # Change related_name to avoid conflict
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",  # Change related_name to avoid conflict
        blank=True
    )

    def __str__(self):
        return self.username
