from django.contrib import admin
from payments.models import TransactionType, Transaction, OrderType, Order


# Register your models here.
@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    class Media:
        fields = '__all__'
        search_fields = '__all__'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    class Media:
        fields = '__all__'
        search_fields = '__all__'


@admin.register(OrderType)
class OrderTypeAdmin(admin.ModelAdmin):
    class Media:
        fields = '__all__'
        search_fields = '__all__'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    class Media:
        fields = '__all__'
        search_fields = '__all__'
