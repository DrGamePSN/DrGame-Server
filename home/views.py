from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .serializers import CartSerializer, AddCartItemSerializer, UpdateCartItemSerializer, CartItemSerializer, \
    CartCreateSerializer
from .models import Cart, CartItem


# cart
class CartDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.filter(is_deleted=False).prefetch_related('cart_items__product__color').all()
    lookup_field = 'id'

    def get(self, request, id):
        cart = get_object_or_404(Cart, id=id)
        if cart.is_deleted:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return self.retrieve(request, cart)


class CartCreateAPIView(generics.CreateAPIView):
    serializer_class = CartCreateSerializer
    queryset = Cart.objects.filter(is_deleted=False).all()


class CartDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.filter(is_deleted=False).all()
    lookup_field = 'id'


# cart-item

class CartItemListAPIView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.select_related('product__color', 'cart').filter(is_deleted=False).all()

    def get(self, request, id):
        cart = get_object_or_404(Cart, id=id)
        cart_items = CartItem.objects.filter(cart=cart, is_deleted=False).all()
        serializer = self.serializer_class(cart_items, many=True)
        return Response(serializer.data)


class CartItemDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.select_related('product__color', 'cart').filter(is_deleted=False).all()

    def get(self, request, id, pk):
        cart = get_object_or_404(Cart, id=id)
        cart_item = CartItem.objects.get(cart=cart, pk=pk, is_deleted=False)
        serializer = self.serializer_class(cart_item)
        return Response(serializer.data)


class CartItemAddCreateAPIView(generics.CreateAPIView):
    serializer_class = AddCartItemSerializer
    queryset = CartItem.objects.select_related('product__color', 'cart').filter(is_deleted=False).all()

    def post(self, request, id):
        cart = get_object_or_404(Cart.objects.filter(is_deleted=False), id=id)
        created_serializer = self.serializer_class(data=request.data, context={'cart': cart})
        created_serializer.is_valid(raise_exception=True)
        created_item = created_serializer.save()
        serializer = CartItemSerializer(created_item)
        return Response(serializer.data)


class CartItemUpdateAPIView(generics.UpdateAPIView):
    queryset = CartItem.objects.select_related('product__color', 'cart').filter(is_deleted=False).all()
    serializer_class = UpdateCartItemSerializer

    def put(self, request, id, pk):
        cart = get_object_or_404(Cart, id=id)
        try:
            cart_item = CartItem.objects.get(cart=cart, pk=pk)
            updated_serializer = self.serializer_class(cart_item, data=request.data)
            updated_serializer.is_valid(raise_exception=True)
            updated_item = updated_serializer.save()
            serializer = CartItemSerializer(updated_item)
            return Response(serializer.data)

        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CartItemDeleteAPIView(generics.DestroyAPIView):
    queryset = CartItem.objects.select_related('product__color', 'cart').filter(is_deleted=False).all()
    serializer_class = CartItemSerializer

    def delete(self, request, id, pk):
        cart = get_object_or_404(Cart, id=id)
        try:
            cart_item = CartItem.objects.get(cart=cart, pk=pk)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
