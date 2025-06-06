from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Customer, BusinessCustomer
from .serializers import (
    CustomerProfileSerializer,
    BusinessCustomerUpgradeSerializer,
    OrderSerializer,
    GameOrderSerializer,
    RepairOrderSerializer,
    TransactionSerializer, BusinessCustomerProfileSerializer
)


class CustomerProfileRetrieveAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:

            return BusinessCustomer.objects.get(user=self.request.user)
        except BusinessCustomer.DoesNotExist:

            return get_object_or_404(Customer, user=self.request.user)

    def get_serializer_class(self):
        if isinstance(self.request.user, BusinessCustomer):
            return BusinessCustomerProfileSerializer
        return CustomerProfileSerializer


# class CustomerProfileUpdateAPIView(generics.UpdateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_object(self):
#         try:
#
#             return BusinessCustomer.objects.get(user=self.request.user)
#         except BusinessCustomer.DoesNotExist:
#
#             return get_object_or_404(Customer, user=self.request.user)
#
#     def get_serializer_class(self):
#         if isinstance(self.request.user, BusinessCustomer):
#             return BusinessCustomerProfileSerializer
#         return CustomerProfileSerializer
