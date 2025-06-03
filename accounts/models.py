import secrets
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from accounts.manager import CustomUserManager


# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    phone = models.CharField(max_length=11, unique=True, verbose_name="phone",null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone


class MainManager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    access = models.CharField(max_length=1, choices=(('1', '1'),), unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.name


class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='otps')
    code = models.CharField(max_length=8)  # برای OTP 8 رقمی
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() <= self.expires_at


class APIKey(models.Model):
    key = models.CharField(max_length=70, unique=True)
    client_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client_name} - {self.key[:10]}..."

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_urlsafe(52)[:70]  # تولید رشته رندوم 70 کاراکتری
        super().save(*args, **kwargs)
