from django.urls import path

from . import views

urlpatterns = [
    #list urls
    path('cart/<uuid:id>/items/',views.CartItemListAPIView.as_view(),name = 'cart-item-list'),
    # retrieve urls
    path('cart/<uuid:id>/', views.CartDetailAPIView.as_view(), name='cart-detail'),
    path('cart/<uuid:id>/items/<int:pk>/', views.CartItemDetailAPIView.as_view(), name='cart-item-detail'),
    # create urls
    path('cart/add/', views.CartCreateAPIView.as_view(), name='cart-create'),
    path('cart/<uuid:id>/items/add/', views.CartItemAddCreateAPIView.as_view(), name='cart-item-create'),
    # update urls
    path('cart/<uuid:id>/items/<int:pk>/update/', views.CartItemUpdateAPIView.as_view(), name='cart-item-update'),
    # delete urls
    path('cart/delete/<uuid:id>/', views.CartDeleteAPIView.as_view(), name='cart-delete')

]
