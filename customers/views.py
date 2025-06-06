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

            return BusinessCustomer.objects.get(user=self.request.user, is_deleted = False)
        except BusinessCustomer.DoesNotExist:

            return get_object_or_404(Customer, user=self.request.user , is_deleted = False)

    def get_serializer_class(self):
        if isinstance(self.request.user, BusinessCustomer):
            return BusinessCustomerProfileSerializer
        return CustomerProfileSerializer


class UpgradeToBusinessCustomerCreateAPIView(generics.CreateAPIView):

    serializer_class = BusinessCustomerUpgradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = BusinessCustomer.objects.select_related('user').all()

    def create(self, request, *args, **kwargs):
        customer = get_object_or_404(Customer , user = request.user)
        serializer = BusinessCustomerUpgradeSerializer(data = request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        customer.is_deleted = True
        customer.save()

        return Response(
            {'status': 'success', 'message': 'Upgraded to business customer successfully'},
            status=status.HTTP_201_CREATED
        )


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
