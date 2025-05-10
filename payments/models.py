from django.db import models
from accounts.models import CustomUser
from customers.models import Customer


# Create your models here.

class OrderType(models.Model):
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order_type = models.ForeignKey(OrderType, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'سفارش {self.customer.full_name} بابت {self.order_type.title}'


class GameOrderType(models.Model):
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class GameOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order_type = models.ForeignKey(OrderType, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'سفارش {self.customer.full_name} بابت {self.order_type.title}'


class RepairOrderType(models.Model):
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class RepairOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order_type = models.ForeignKey(OrderType, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'سفارش {self.customer.full_name} بابت {self.order_type.title}'


class TransactionType(models.Model):
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Transaction(models.Model):
    payer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='payer')
    receiver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='receiver')
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=3)
    status = models.CharField(max_length=10, null=True, choices=(
        ('Success', 'موفق'),
        ('Suspended', 'تعلیق'),
        ('Cancelled', 'کنسل شده'),
        ('Failed', 'ناموفق')
    ))
    game_order = models.ForeignKey(GameOrder, on_delete=models.SET_NULL, null=True, related_name='game_order')
    repair_order = models.ForeignKey(RepairOrder, on_delete=models.SET_NULL, null=True, related_name='repair_order')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='order')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.transaction_type.title}: {self.amount} - {self.description}'
