from rest_framework import serializers
from .models import Cart, CartItem
from storage.models import Product, ProductColor


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id']
        read_only_fields = ['id', ]


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

    def create(self, validated_data):
        cart = self.context['cart']
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        try:
            cart_item = CartItem.objects.get(product=product, cart = cart)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart=cart, **validated_data)

        self.instance = cart_item
        return cart_item
