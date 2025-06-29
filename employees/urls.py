from django.urls import path
from employees import views

urlpatterns = [
    path('order-list/', views.OrderList.as_view(), name='order-list'),
]