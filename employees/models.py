from django.db import models

from accounts.models import CustomUser


# Create your models here.
class EmployeeRole(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)
    type = models.CharField(max_length=100, choices=(
        ('operational', 'عملیاتی'),
        ('in organ', 'درون سازمانی')
    ), null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.ForeignKey(EmployeeRole, on_delete=models.SET_NULL, null=True)
    profile_picture = models.ImageField(null=True, upload_to='profile_pictures/employees/')
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    national_code = models.CharField(max_length=10, null=True)
    employee_id = models.CharField(max_length=11, null=True)
    balance = models.FloatField(null=True)
    income_type = models.CharField(max_length=20, choices=(
        ('Commission', 'پورسانت'),
        ('Fixed salary', 'حقوق ثابت')
    ), null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Repairman(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(null=True, upload_to='profile_pictures/repairmen/')
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    national_code = models.CharField(max_length=10, null=True)
    balance = models.FloatField(null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class EmployeeFile(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField(upload_to='employee_files/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.employee}: {self.title}'


class EmployeeTask(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=20, choices=(
        ('Personal', 'شخصی'),
        ('Organize', 'سازمانی')
    ), null=True, blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    status = models.CharField(max_length=20, choices=(
        ('planed', 'برنامه ریزی شده'),
        ('in progress', 'در حال انجام'),
        ('done', 'انجام شده')
    ))
    deadline = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.employee}: {self.title}'
