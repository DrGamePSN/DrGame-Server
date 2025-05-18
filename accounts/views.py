from rest_framework import generics

from accounts.serializers import EmployeeListSerializer, SonyAccountSerializer, ProductCategorySerializer, \
    ProductSerializer, EmployeeSerializer, RepairmanSerializer, CustomerSerializer, BusinessCustomerSerializer
from customers.models import Customer, BusinessCustomer
from employees.models import Employee, Repairman
from payments.models import Transaction, TransactionType
from storage.models import SonyAccount, ProductCategory


class EmployeeListAPIView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeListSerializer


class EmployeeDetailAPIView(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'employee_id'


class RepairmanListAPIView(generics.ListAPIView):
    queryset = Repairman.objects.all()
    serializer_class = RepairmanSerializer


class RepairmanDetailAPIView(generics.RetrieveAPIView):
    queryset = Repairman.objects.all()
    serializer_class = RepairmanSerializer
    lookup_field = 'pk'

class CustomerListAPIView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetailAPIView(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'pk'

class BusinessCustomerListAPIView(generics.ListAPIView):
    queryset = BusinessCustomer.objects.all()
    serializer_class = BusinessCustomerSerializer

class BusinessCustomerDetailAPIView(generics.RetrieveAPIView):
    queryset = BusinessCustomer.objects.all()
    serializer_class = BusinessCustomerSerializer
    lookup_field = 'pk'
class SonyAccountListAPIView(generics.ListAPIView):
    queryset = SonyAccount.objects.all()
    serializer_class = SonyAccountSerializer


class SonyAccountDetailAPIView(generics.RetrieveAPIView):
    queryset = SonyAccount.objects.all()
    serializer_class = SonyAccountSerializer
    lookup_field = 'pk'


class ProductCategoryListAPIView(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


class TransactionListAPIView(generics.ListAPIView):
    queryset = TransactionType.objects.all()
    serializer_class = ProductCategorySerializer


class TransactionDetailAPIView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
