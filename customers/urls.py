from django.urls import path

from . import views

urlpatterns = [
    # read urls
    path('profile/', views.CustomerProfileRetrieveAPIView.as_view(), name='profile'),
    path('profile/upgrade/', views.UpgradeToBusinessCustomerCreateAPIView.as_view(), name='upgrade-to-business'),
    # path('profile/update/', views.CustomerProfileUpdateAPIView.as_view(), name='profile-update'),

]
