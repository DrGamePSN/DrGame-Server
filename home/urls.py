from django.urls import path

from . import views

urlpatterns = [
    # retrieve urls
    path('cart/detail/<uuid:id>/', views.CartDetailAPIView.as_view(), name='cart-detail'),
    # create urls
    path('cart/add/', views.CartCreateAPIView.as_view(), name='cart-create'),
    # delete urls
    path('cart/delete/<uuid:id>/', views.CartDeleteAPIView.as_view(), name='cart-delete')

]
