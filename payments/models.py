from django.db import models

from home.models import Course
from storage.models import CustomerConsole, Product
from accounts.models import CustomUser
from customers.models import Customer
from django.conf import settings


# Create your models here.

class OrderType(models.Model):
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order_type = models.ForeignKey(OrderType, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=3)
    description = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'سفارش {self.customer.full_name} بابت {self.order_type.title}'


class GameOrderType(models.Model):
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class GameOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order_type = models.ForeignKey(GameOrderType, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=3)
    product = models.ForeignKey(CustomerConsole, on_delete=models.SET_NULL, null=True)
    games_count = models.IntegerField(default=0, null=True, blank=True)
    selected_games_count = models.IntegerField(default=0, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'سفارش {self.customer.full_name} بابت {self.order_type.title}'


class RepairOrderType(models.Model):
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class RepairOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order_type = models.ForeignKey(RepairOrderType, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=3)
    product = models.ForeignKey(CustomerConsole, on_delete=models.SET_NULL, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'سفارش {self.customer.full_name} بابت {self.order_type.title}'


class CourseOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='orders')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order #{self.id} - {self.customer} - {self.course}'


class TransactionType(models.Model):
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    is_deleted = models.BooleanField(default=False)
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
    game_order = models.ForeignKey(GameOrder, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name='game_order')
    repair_order = models.ForeignKey(RepairOrder, on_delete=models.SET_NULL, blank=True, null=True,
                                     related_name='repair_order')
    course_order = models.ForeignKey(CourseOrder, on_delete=models.SET_NULL, blank=True, null=True,
                                     related_name='course_order')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='order')
    description = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.transaction_type.title}: {self.amount} - {self.description}'
