from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .serializers import CartSerializer
from .models import Cart


class CartDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    lookup_field = 'id'

    def get(self, request, id):
        cart = get_object_or_404(Cart, id=id)
        if cart.is_deleted:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return self.retrieve(request, cart)


class CartCreateAPIView(generics.CreateAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()


class CartDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    lookup_field = 'id'

    def delete(self, request, id):
        cart = get_object_or_404(Cart, id=id)
        cart.is_deleted = True
        cart.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
