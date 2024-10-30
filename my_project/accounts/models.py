from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    # Add your custom fields here
    ...

    # Override related_name for groups and user_permissions
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Unique related_name for groups
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Unique related_name for user_permissions
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
