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
    title = models.CharField(max_length=255)

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
    author = models.CharField(max_length=255, blank = True)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
