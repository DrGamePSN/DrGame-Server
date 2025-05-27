from django.urls import path

from . import views

# cart / cart-items / blog
urlpatterns = [
    # list urls
    path('cart/<uuid:id>/items/', views.CartItemListAPIView.as_view(), name='cart-item-list'),
    path('blog/categories/', views.BlogCategoryListAPIView.as_view(), name='blog-category-list'),
    path('blog/posts/', views.BlogPostListAPIView.as_view(), name='blog-post-list'),

    # retrieve urls

    path('cart/<uuid:id>/', views.CartDetailAPIView.as_view(), name='cart-detail'),
    path('cart/<uuid:id>/items/<int:pk>/', views.CartItemDetailAPIView.as_view(), name='cart-item-detail'),
    path('blog/posts/<int:pk>/', views.BlogPostRetrieveAPIView.as_view(), name='blog-post-detail'),

    # create urls

    path('cart/add/', views.CartCreateAPIView.as_view(), name='cart-create'),
    path('cart/<uuid:id>/items/add/', views.CartItemAddCreateAPIView.as_view(), name='cart-item-create'),
    path('blog/categories/add/', views.BlogCategoryCreateAPIView.as_view(), name='blog-category-create'),
    path('blog/posts/add/', views.BlogPostCreateAPIView.as_view(), name='blog-post-create'),

    # update urls

    path('cart/<uuid:id>/items/<int:pk>/update/', views.CartItemUpdateAPIView.as_view(), name='cart-item-update'),
    path('blog/categories/<int:pk>/update/', views.BlogCategoryUpdateAPIView.as_view(), name='blog-category-update'),
    path('blog/posts/<int:pk>/update/', views.BlogPostUpdateAPIView.as_view(), name='blog-post-update'),

    # delete urls

    path('cart/<uuid:id>/delete/', views.CartDeleteAPIView.as_view(), name='cart-delete'),
    path('cart/<uuid:id>/items/<int:pk>/delete/', views.CartItemDeleteAPIView.as_view(), name='cart-item-delete'),
    path('blog/categories/<int:pk>/delete/', views.BlogCategoryDeleteAPIView.as_view(), name='blog-category-delete'),
    path('blog/posts/<int:pk>/delete/', views.BlogPostDeleteAPIView.as_view(), name='blog-post-delete'),
]
