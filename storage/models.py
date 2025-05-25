from django.db import models

from customers.models import Customer


# Create your models here.

class ProductCategory(models.Model):
    title = models.CharField(max_length=100, unique=True, null=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    img = models.ImageField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProductColor(models.Model):
    title = models.CharField(max_length=100, unique=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProductCompany(models.Model):
    title = models.CharField(max_length=100, unique=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100, unique=True, null=True)
    main_img = models.ImageField(null=True, blank=True, upload_to='main_img/products/')
    description = models.TextField(max_length=5000, null=True, blank=True)
    color = models.ForeignKey(ProductColor, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(ProductCompany, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(decimal_places=5, max_digits=20)
    stock = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} {self.color.title}'


class ProductImage(models.Model):
    img = models.ImageField(null=True, blank=True, upload_to='images/products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title


class SonyAccountStatus(models.Model):
    title = models.CharField(max_length=100, unique=True, null=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class SonyAccountBank(models.Model):
    title = models.CharField(max_length=200, unique=True, null=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Game(models.Model):
    title = models.CharField(max_length=100, unique=True, null=True)
    main_img = models.ImageField(null=True, blank=True, upload_to="main_img/game/")
    description = models.TextField(max_length=5000, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class GameImage(models.Model):
    img = models.ImageField(null=True, blank=True, upload_to='images/games/')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.game.title


class SonyAccount(models.Model):
    username = models.CharField(max_length=100, unique=True, null=True)
    password = models.CharField(max_length=100, null=True)
    two_step = models.IntegerField(null=True, blank=True)
    status = models.ForeignKey(SonyAccountStatus, on_delete=models.SET_NULL, null=True, blank=True)
    bank_account_status = models.BooleanField(null=True, blank=True)
    bank_account = models.ForeignKey(SonyAccountBank, on_delete=models.SET_NULL, null=True, blank=True)
    plus = models.BooleanField(null=True, blank=True)
    games = models.ManyToManyField(Game, through='SonyAccountGame', related_name='accounts')
    region = models.CharField(max_length=100, null=True, blank=True, choices=(
        ('America', 'america'),
        ('Europe', 'europe'),
        ('Asia', 'asia'),
        ('Mix', 'mix'),
    ))
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class SonyAccountGame(models.Model):
    sony_account = models.ForeignKey(SonyAccount, on_delete=models.CASCADE, related_name='account_games')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_accounts')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['sony_account', 'game']
        indexes = [
            models.Index(fields=['sony_account', 'game']),
        ]

    def __str__(self):
        return f"{self.sony_account} - {self.game}"


class CustomerConsole(models.Model):
    owner = models.OneToOneField(Customer, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, choices=(
        ('Sony', 'Sony'),
        ('X-Box', 'X-Box'),
        ('Nintendo', 'Nintendo'),
    ), blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + ' ' + self.owner.full_name
