from rest_framework import serializers
from .models import Cart, CartItem, BlogCategory
from storage.models import Product, ProductColor


# cart-item
class ProductColorCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['title']


class ProductCartItemSerializer(serializers.ModelSerializer):
    color = ProductColorCartItemSerializer()

    class Meta:
        model = Product
        fields = ['title', 'color', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductCartItemSerializer()
    total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'total', ]

    def get_total(self, obj):
        return obj.total_item_price


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

    def validate(self, data):
        product_item = data['product']
        product = Product.objects.get(pk=product_item.pk)
        if data['quantity'] > product.stock:
            raise serializers.ValidationError('out of stock!')
        return data

    def create(self, validated_data):
        cart_id = self.context['cart']
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        try:
            cart_item = CartItem.objects.get(product=product, cart_id=cart_id)
            current_quantity = cart_item.quantity
            if (current_quantity + quantity) > product.stock:
                raise serializers.ValidationError('out of stock!')
            else:
                cart_item.quantity += quantity
                cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart_id=cart_id, **validated_data)

        self.instance = cart_item
        return cart_item


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity', ]

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value

    def validate(self, data):
        cart_item = self.instance

        # Check product stock
        if 'quantity' in data and data['quantity'] > cart_item.product.stock:
            raise serializers.ValidationError({
                'quantity': f"Only {cart_item.product.stock} items available in stock"
            })
        return data


# cart

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'cart_items', 'total_price']
        read_only_fields = ['id', 'cart_items', 'total_price']

    def get_total_price(self, obj):
        return obj.total_price


class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id']
        read_only_fields = ['id']


# blog
class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['title']
