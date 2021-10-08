# DB classes
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import (
    AbstractUser, PermissionsMixin
)
# from rest_framework_simplejwt.authentication import TODO: ASK ARMEN
from accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=254, unique=True)
    # profile_picture = models.ImageField()  # inch parameter em specify anum?
    phone_number = models.CharField(max_length=10, blank=False, null=False, unique=True,
                                    validators=[RegexValidator(regex=r"^\d{10}$")])

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
