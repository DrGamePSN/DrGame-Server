from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_deleted', 'created_at']


@admin.register(CartItem)
class CartAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'is_deleted', 'updated_at', ]
