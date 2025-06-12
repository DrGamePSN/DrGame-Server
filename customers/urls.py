from django.urls import path

from . import views

urlpatterns = [
    path('profile/create/', views.CustomerProfileCreateAPIView.as_view(), name='create-customer-profile'),
    path('profile/', views.CustomerProfileRetrieveAPIView.as_view(), name='profile'),
    path('profile/upgrade/', views.UpgradeToBusinessCustomerCreateAPIView.as_view(), name='upgrade-to-business'),

    # order list & retrieve urls
    path('orders/', views.CustomerOrderListAPIView.as_view(), name='customer-orders'),
    path('orders/<int:pk>/', views.CustomerOrderRetrieveAPIView.as_view(), name='customer-order-detail'),

    # game order list & retrieve urls
    path('orders/game/', views.CustomerGameOrderListAPIView.as_view(), name='game-orders'),
    path('orders/game/<int:pk>/', views.CustomerGameOrderRetrieveAPIView.as_view(), name='game-order-detail'),

    # repair order list & retrieve urls
    path('orders/repair/', views.CustomerRepairOrderListAPIView.as_view(), name='repair-orders'),
    path('orders/repair/<int:pk>/', views.CustomerRepairOrderRetrieveAPIView.as_view(), name='repair-order-detail'),

    # course order list & retrieve urls
    path('orders/course/', views.CustomerCourseOrderListAPIView.as_view(), name='course-orders'),
    path('orders/course/<int:pk>/', views.CustomerCourseOrderRetrieveAPIView.as_view(), name='course-order-detail'),

    # transactions
    path('transactions/', views.CustomerTransactionListAPIView.as_view(), name='customer-transactions'),
    path('transactions/<int:pk>/', views.CustomerTransactionRetrieveAPIView.as_view(),
         name='customer-transactions-detail'),

    #
    # # Transactions
    # path('transactions/', CustomerTransactionListAPIView.as_view(), name='customer-transactions'),
    # # path('profile/update/', views.CustomerProfileUpdateAPIView.as_view(), name='profile-update'),

]
