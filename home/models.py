from django.core.validators import EmailValidator
from django.conf import settings
from django.db import models
from uuid import uuid4
from ckeditor.fields import RichTextField
from django.utils import timezone
from slugify import slugify

from storage.models import Product, ProductColor


# Shopping

class CartManager(models.Manager):
    def get_user_cart(self, request):
        if request.user.is_authenticated:
            cart, created = self.get_or_create(user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            cart, created = self.get_or_create(session_key=request.session.session_key,
                                               is_deleted=False,
                                               user=None,
                                               )

        return cart


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    objects = CartManager()

    class Meta:
        unique_together = [['user'], ['session_key']]

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Cart (session: {self.session_key})"

    @property
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.cart_items.all())



# Cart.objects = CartManager()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(default=1)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['cart', 'product']]

    @property
    def total_item_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f'{self.product} : {self.quantity}'


# Blog

class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(max_length=150, unique=True, allow_unicode=True, verbose_name="اسلاگ")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BlogTag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="نام تگ")
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name="اسلاگ")

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    STATUS_CHOICES = (
        ('draft', 'پیش‌نویس'),
        ('published', 'منتشر شده'),
    )

    title = models.CharField(max_length=200, unique=True, verbose_name="عنوان")
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True, verbose_name="اسلاگ")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts',
                               verbose_name="نویسنده")
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='posts',
                                 verbose_name="دسته‌بندی")
    tags = models.ManyToManyField(BlogTag, blank=True, related_name='posts', verbose_name="تگ‌ها")
    content = models.TextField(verbose_name="محتوا")
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name="تصویر شاخص")
    meta_description = models.CharField(max_length=160, blank=True, null=True, verbose_name="توضیحات متا")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")
    published_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ انتشار")

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-published_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# about us & contact us models

class AboutUs(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    content = RichTextField()

    # Media
    banner_image = models.ImageField(upload_to='about/banners/', null=True, blank=True)
    team_image = models.ImageField(upload_to='about/team/', null=True, blank=True)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "About Us Page"

    def __str__(self):
        return self.title


class ContactUs(models.Model):
    address = models.CharField(max_length=700)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    map_embed_code = models.TextField(blank=True, help_text="Google Maps iframe code")

    # Business Hours
    opening_hours = models.CharField(max_length=100, default="9:00 AM - 6:00 PM")

    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Contact Page Settings"

    def __str__(self):
        return f'{self.address} - {self.phone}'


class ContactSubmission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    subject = models.CharField(max_length=200)
    message = models.TextField()

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"

    def __str__(self):
        return f'{self.email} : {self.subject}'


# Course Models

class Course(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, )
    description = RichTextField()
    course_image = models.ImageField(upload_to='course/', )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Video(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('private', 'Private'),
    ]
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, )
    description = RichTextField(blank=True)
    video_file = models.FileField(upload_to='videos/', )
    status = models.CharField(choices=STATUS_CHOICES, max_length=10)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    duration = models.DurationField()
    priority = models.PositiveIntegerField(unique=True, verbose_name='video order')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} - {self.course.title}'


class CourseOrder(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='orders')
    payment_status = models.CharField(choices=PAYMENT_STATUS, max_length=10, default='pending')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order #{self.id} - {self.user} - {self.course}'
