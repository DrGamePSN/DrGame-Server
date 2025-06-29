from django.shortcuts import render
from django.views import generic
from rest_framework import generics
from rest_framework.permissions import AllowAny

from employees.serializers import OrderListSerializer
from payments.models import GameOrder


# Create your views here.
class OrderList(generics.ListAPIView):
    queryset = GameOrder.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [AllowAny]
