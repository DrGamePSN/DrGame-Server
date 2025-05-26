from django.contrib import admin
from .models import Cart, CartItem , BlogCategory , BlogPost


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_deleted', 'created_at']


@admin.register(CartItem)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','cart', 'product', 'quantity', 'is_deleted', 'updated_at', ]

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at' , 'is_deleted']

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category','author','is_deleted','created_at']


