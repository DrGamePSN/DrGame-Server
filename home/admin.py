from django.contrib import admin

from payments.models import CourseOrder
from .models import Cart, CartItem, BlogCategory, BlogPost, ContactUs, AboutUs, ContactSubmission, BlogTag, Course, \
    Video, HomeBanner


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_deleted', 'created_at']


@admin.register(CartItem)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity', 'is_deleted', 'updated_at', ]


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'name', 'created_at', 'is_deleted']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'title', 'category', 'author', 'status', 'created_at']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


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


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'description', 'price', 'status', 'created_at', 'updated_at', ]
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'description', 'status', 'course', 'duration', 'priority', 'created_at',
                    'updated_at', ]
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['priority']


@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_chosen', 'order')
    list_editable = ('is_chosen', 'order')
    list_filter = ('is_chosen',)
    search_fields = ('title',)


@admin.register(CourseOrder)
class CourseOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'payment_status', 'price', 'created_at', 'updated_at']
