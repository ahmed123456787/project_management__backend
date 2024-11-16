from django.contrib.auth.models import AbstractBaseUser, Group, PermissionsMixin,BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Create the user manager for the user"""
    def create_user(self, email, password=None,**extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_superuser= True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
    
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD= "email"
    objects = UserManager()

    def __str__(self):
        return self.email