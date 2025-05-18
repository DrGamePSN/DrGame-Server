from django.urls import path

from accounts.views import EmployeeListAPIView, EmployeeDetailAPIView, RepairmanListAPIView, RepairmanDetailAPIView, \
    SonyAccountListAPIView, SonyAccountDetailAPIView, ProductCategoryListAPIView, ProductDetailAPIView, \
    TransactionListAPIView, TransactionDetailAPIView, CustomerListAPIView, CustomerDetailAPIView, \
    BusinessCustomerListAPIView, BusinessCustomerDetailAPIView

urlpatterns = [
    path('emoployee-list/', EmployeeListAPIView.as_view(), name='employee-list'),
    path('emoployee-detail/<employee_id>', EmployeeDetailAPIView.as_view(), name='employee-detail'),
    path('customer-list/', CustomerListAPIView.as_view(), name='customer-list'),
    path('customer-detail/<int:pk>', CustomerDetailAPIView.as_view(), name='customer-detail'),
    path('business-customer-list/', BusinessCustomerListAPIView.as_view(), name='business-customer-list'),
    path('business-customer-detail/<int:pk>', BusinessCustomerDetailAPIView.as_view(), name='business-customer-detail'),
    path('repairman-list/', RepairmanListAPIView.as_view(), name='repairman-list'),
    path('repairman-detail/<int:pk>', RepairmanDetailAPIView.as_view(), name='repairman-detail'),
    path('sony-account-list/', SonyAccountListAPIView.as_view(), name='sony-account-list'),
    path('sony-account-detail/<int:pk>', SonyAccountDetailAPIView.as_view(), name='sony-account-detail'),
    path('product-list/', ProductCategoryListAPIView.as_view(), name='product-list'),
    path('product-detail/<int:pk>', ProductDetailAPIView.as_view(), name='product-detail'),
    path('transaction-list/', TransactionListAPIView.as_view(), name='transaction-list'),
    path('transaction-detail/<int:pk>', TransactionDetailAPIView.as_view(), name='transaction-detail'),

]
