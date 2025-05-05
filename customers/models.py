from django.db import models


# Create your models here.

class Customer(models.Model):
    full_name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True, unique=True)
    address = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profile_pics/customers/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class BusinessCustomer(models.Model):
    full_name = models.CharField(max_length=50, null=True, blank=True)
    license = models.FileField(null=True, blank=True, upload_to='business/license/')
    phone_number = models.CharField(max_length=11, null=True, blank=True, unique=True)
    address = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profile_pics/customers/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
