from django.urls import path

from . import views

# cart / cart-items / blog / contact / about

urlpatterns = [
    # ==================== Cart URLs ====================
    path('cart/', views.CartCreateAPIView.as_view(), name='cart-create'),
    path('cart/<uuid:id>/', views.CartDetailAPIView.as_view(), name='cart-detail'),
    path('cart/<uuid:id>/delete/', views.CartDeleteAPIView.as_view(), name='cart-delete'),

    # Cart Items
    path('cart/<uuid:id>/items/', views.CartItemListAPIView.as_view(), name='cart-item-list'),
    path('cart/<uuid:id>/items/add/', views.CartItemAddCreateAPIView.as_view(), name='cart-item-create'),
    path('cart/<uuid:id>/items/<int:pk>/', views.CartItemDetailAPIView.as_view(), name='cart-item-detail'),
    path('cart/<uuid:id>/items/<int:pk>/update/', views.CartItemUpdateAPIView.as_view(), name='cart-item-update'),
    path('cart/<uuid:id>/items/<int:pk>/delete/', views.CartItemDeleteAPIView.as_view(), name='cart-item-delete'),

    # ==================== Blog URLs ====================
    # Categories
    path('blog/categories/', views.BlogCategoryListAPIView.as_view(), name='blog-category-list'),
    path('blog/categories/add/', views.BlogCategoryCreateAPIView.as_view(), name='blog-category-create'),
    path('blog/categories/<int:pk>/update/', views.BlogCategoryUpdateAPIView.as_view(), name='blog-category-update'),
    path('blog/categories/<int:pk>/delete/', views.BlogCategoryDeleteAPIView.as_view(), name='blog-category-delete'),

    # Posts
    path('blog/posts/', views.BlogPostListAPIView.as_view(), name='blog-post-list'),
    path('blog/posts/add/', views.BlogPostCreateAPIView.as_view(), name='blog-post-create'),
    path('blog/posts/<int:pk>/', views.BlogPostRetrieveAPIView.as_view(), name='blog-post-detail'),
    path('blog/posts/<int:pk>/update/', views.BlogPostUpdateAPIView.as_view(), name='blog-post-update'),
    path('blog/posts/<int:pk>/delete/', views.BlogPostDeleteAPIView.as_view(), name='blog-post-delete'),

    # Nested Category Posts
    path('blog/categories/<int:category_id>/posts/', views.BlogPostListByCategoryAPIView.as_view(),
         name='blog-category-posts-list'),
    path('blog/categories/<int:category_id>/posts/<int:pk>/', views.BlogPostRetrieveByCategoryAPIView.as_view(),
         name='blog-category-posts-detail'),

    # ==================== Content Pages ====================
    path('about-us/', views.AboutUsRetrieveAPIView.as_view(), name='about-us'),
    path('about-us/update/', views.AboutUsUpdateAPIView.as_view(), name='about-us-update'),

    path('contact-us/', views.ContactUsRetrieveAPIView.as_view(), name='contact-us'),
    path('contact/submit/', views.ContactSubmissionCreateAPIView.as_view(), name='contact-submit'),
]



