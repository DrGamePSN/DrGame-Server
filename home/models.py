from django.core.validators import EmailValidator
from django.conf import settings
from django.db import models
from uuid import uuid4
from ckeditor.fields import RichTextField

from storage.models import Product, ProductColor


# Shopping
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.cart_items.all())


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
    title = models.CharField(max_length=255, unique=True)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    main_img = models.ImageField(null=True, blank=True, upload_to='main_img/blog/')
    description = RichTextField()
    category = models.ForeignKey(BlogCategory, on_delete=models.PROTECT, related_name='posts')
    author = models.CharField(max_length=255, blank=True)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

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
