from django.contrib import admin
from employees import models


# Register your models here.
@admin.register(models.EmployeeRole)
class EmployeeRoleAdmin(admin.ModelAdmin):
    class Meta:
        fields = '__all__'
        search_fields = '__all__'


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    class Meta:
        fields = '__all__'
        search_fields = '__all__'


@admin.register(models.Repairman)
class RepairmanAdmin(admin.ModelAdmin):
    class Meta:
        fields = '__all__'
        search_fields = '__all__'
