from django.urls import path

from . import views

# cart / cart-items / blog
urlpatterns = [
    # list urls
    path('cart/<uuid:id>/items/', views.CartItemListAPIView.as_view(), name='cart-item-list'),
    path('blog/categories/', views.BlogCategoryListAPIView.as_view(), name='blog-category-list'),

    # retrieve urls

    path('cart/<uuid:id>/', views.CartDetailAPIView.as_view(), name='cart-detail'),
    path('cart/<uuid:id>/items/<int:pk>/', views.CartItemDetailAPIView.as_view(), name='cart-item-detail'),

    # create urls

    path('cart/add/', views.CartCreateAPIView.as_view(), name='cart-create'),
    path('cart/<uuid:id>/items/add/', views.CartItemAddCreateAPIView.as_view(), name='cart-item-create'),
    path('blog/categories/add/', views.BlogCategoryCreateAPIView.as_view(), name='blog-category-create'),

    # update urls

    path('cart/<uuid:id>/items/<int:pk>/update/', views.CartItemUpdateAPIView.as_view(), name='cart-item-update'),
    path('blog/categories/<int:pk>/update/', views.BlogCategoryUpdateAPIView.as_view(), name='blog-category-update'),

    # delete urls

    path('cart/<uuid:id>/delete/', views.CartDeleteAPIView.as_view(), name='cart-delete'),
    path('cart/<uuid:id>/items/<int:pk>/delete/', views.CartItemDeleteAPIView.as_view(), name='cart-item-delete'),
    path('blog/categories/<int:pk>/delete/', views.BlogCategoryDeleteAPIView.as_view(), name='blog-category-delete'),
]
