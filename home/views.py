from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .serializers import CartSerializer, AddCartItemSerializer
from .models import Cart, CartItem


class CartDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.filter(is_deleted=False).prefetch_related('cart_items').all()
    lookup_field = 'id'

    def get(self, request, id):
        cart = get_object_or_404(Cart, id=id)
        if cart.is_deleted:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return self.retrieve(request, cart)


class CartCreateAPIView(generics.CreateAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.filter(is_deleted=False).all()


class CartDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.filter(is_deleted=False).all()
    lookup_field = 'id'

    def delete(self, request, id):
        cart = get_object_or_404(Cart, id=id)
        cart.is_deleted = True
        cart.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# cart-item
class CartItemAddCreateAPIView(generics.CreateAPIView):
    serializer_class = AddCartItemSerializer
    queryset = CartItem.objects.select_related('product', 'cart', 'colors').filter(is_deleted=False).all()

    def post(self, request, id):
        cart = get_object_or_404(Cart.objects.filter(is_deleted=False), id=id)
        serializer = self.serializer_class(data=request.data, context={'cart': cart})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    # def get_serializer_context(self, id):
    #     cart = get_object_or_404(Cart.objects.filter(is_deleted=False), id=id)
    #     return {'cart': cart}
