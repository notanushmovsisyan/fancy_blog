from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import (
    AbstractUser, PermissionsMixin
)
from accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=254, unique=True)

    image = models.ImageField(upload_to='media/', blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=False, null=False, unique=True,
                                    validators=[RegexValidator(regex=r"^\d{10}$")])

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
