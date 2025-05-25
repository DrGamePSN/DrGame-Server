from django.db import models
from uuid import uuid4

from storage.models import Product


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(default=1)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = [['cart', 'product']]
