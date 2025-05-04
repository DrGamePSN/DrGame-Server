from customers.models import BusinessCustomer, Customer
from django.contrib import admin


# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    class Meta:
        fields = "__all__"
        search_fields = "__all__"


@admin.register(BusinessCustomer)
class BusinessCustomerAdmin(admin.ModelAdmin):
    class Meta:
        fields = "__all__"
        search_fields = "__all__"
