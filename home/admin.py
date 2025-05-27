from django.contrib import admin
from .models import Cart, CartItem, BlogCategory, BlogPost, ContactUs, AboutUs, ContactSubmission


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_deleted', 'created_at']


@admin.register(CartItem)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity', 'is_deleted', 'updated_at', ]


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'is_deleted']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'author', 'is_deleted', 'created_at']


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'subtitle', 'content', 'created_at', ]

    def has_add_permission(self, request):
        return not AboutUs.objects.exists()


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'phone', 'email', 'opening_hours', 'instagram_url', 'created_at']

    def has_add_permission(self, request):
        return not ContactUs.objects.exists()


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'subject', 'message_preview', 'user', 'is_deleted']

    def message_preview(self, obj):
        return obj.message[:100] + '...' if len(obj.subject) > 10 else obj.message

    message_preview.short_description = 'Message'
