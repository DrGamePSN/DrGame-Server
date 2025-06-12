from django.urls import path

from . import views

# cart / cart-items / blog / contact / about

urlpatterns = [

    # ==================== Store URLs ====================
    path('store/products/', views.ProductListAPIView.as_view(), name='store-product-list'),
    path('store/products/<int:pk>/', views.ProductRetrieveAPIView.as_view(), name='store-product-detail'),

    # ==================== Product Category URLs ====================
    path('store/categories/', views.ProductCategoryListAPIView.as_view(), name='store-category-list'),
    path('store/categories/<int:pk>/', views.ProductCategoryRetrieveAPIView.as_view(), name='store-category-detail'),
    path('store/categories/<int:pro_category>/products/<int:pk>/', views.ProductByCategoryRetrieveAPIView.as_view(),
         name='store-product-by-category-detail'),

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
    path('blog/categories/<str:slug>/update/', views.BlogCategoryUpdateAPIView.as_view(), name='blog-category-update'),
    path('blog/categories/<str:slug>/delete/', views.BlogCategoryDeleteAPIView.as_view(), name='blog-category-delete'),

    # tags
    path('blog/tags/', views.BlogTagListAPIView.as_view(), name='blog-tag-list'),
    path('blog/tags/add/', views.BlogTagCreateAPIView.as_view(), name='blog-tag-create'),
    path('blog/tags/<str:slug>/update/', views.BlogTagUpdateAPIView.as_view(), name='blog-tag-update'),
    path('blog/tags/<str:slug>/delete/', views.BlogTagDeleteAPIView.as_view(), name='blog-tag-delete'),

    # Posts
    path('blog/posts/', views.BlogPostListAPIView.as_view(), name='blog-post-list'),
    path('blog/posts/add/', views.BlogPostCreateAPIView.as_view(), name='blog-post-create'),
    path('blog/posts/<str:slug>/', views.BlogPostRetrieveAPIView.as_view(), name='blog-post-detail'),
    path('blog/posts/<str:slug>/update/', views.BlogPostUpdateAPIView.as_view(), name='blog-post-update'),
    path('blog/posts/<str:slug>/delete/', views.BlogPostDeleteAPIView.as_view(), name='blog-post-delete'),

    # Nested Category Posts
    path('blog/categories/<str:category_slug>/posts/', views.BlogPostListByCategoryAPIView.as_view(),
         name='blog-category-posts-list'),
    path('blog/categories/<str:category_slug>/posts/<str:slug>/', views.BlogPostRetrieveByCategoryAPIView.as_view(),
         name='blog-category-posts-detail'),

    # ==================== Content Pages ====================
    path('about-us/', views.AboutUsRetrieveAPIView.as_view(), name='about-us'),
    path('about-us/add/', views.AboutUsCreateAPIView.as_view(), name='about-us-create'),
    path('about-us/update/', views.AboutUsUpdateAPIView.as_view(), name='about-us-update'),
    path('about-us/delete/', views.AboutUsDeleteAPIView.as_view(), name='about-us-delete'),

    path('contact-us/', views.ContactUsRetrieveAPIView.as_view(), name='contact-us'),
    path('contact-us/add/', views.ContactUsCreateAPIView.as_view(), name='contact-us-create'),
    path('contact-us/update/', views.ContactUsUpdateAPIView.as_view(), name='contact-us-update'),
    path('contact-us/delete/', views.ContactUsDeleteAPIView.as_view(), name='contact-us-delete'),

    path('contact/submit/', views.ContactSubmissionCreateAPIView.as_view(), name='contact-submit'),

    # ==================== Video URLs ====================

    # course
    path('courses/', views.CourseListAPIView.as_view(), name='course-list'),
    path('courses/orders/', views.CourseOrderListAPIView.as_view(), name='course-order-list'),
    path('courses/add/', views.CourseCreateAPIView.as_view(), name='course-create'),

    path('courses/<str:slug>/', views.CourseRetrieveAPIView.as_view(), name='course-detail'),
    path('courses/<str:slug>/update/', views.CourseUpdateAPIView.as_view(), name='course-update'),
    path('courses/<str:slug>/delete/', views.CourseDeleteAPIView.as_view(), name='course-delete'),

    # video
    path('courses/<str:course_slug>/videos/', views.VideoListAPIView.as_view(), name='video-list'),
    path('courses/<str:course_slug>/videos/add/', views.VideoCreateAPIView.as_view(), name='video-create'),
    path('courses/<str:course_slug>/videos/<str:slug>/', views.VideoRetrieveAPIView.as_view(), name='video-detail'),
    path('courses/<str:course_slug>/videos/<str:slug>/update', views.VideoUpdateAPIView.as_view(), name='video-update'),
    path('courses/<str:course_slug>/videos/<str:slug>/delete', views.VideoDeleteAPIView.as_view(), name='video-delete'),

    # Course Order
    path('courses/orders/add/', views.CourseOrderCreateAPIView.as_view(), name='course-order-create'),
    path('courses/orders/<int:pk>/', views.CourseOrderRetrieveAPIView.as_view(), name='course-order-detail'),
    path('courses/orders/<int:pk>/update/', views.CourseOrderUpdateAPIView.as_view(), name='course-order-update'),
    path('courses/orders/<int:pk>/delete/', views.CourseOrderDeleteAPIView.as_view(), name='course-order-delete'),

    # ==================== Game URLs ====================

    # Game Trends List & Retrieve
    path('store/games/', views.GameListAPIView.as_view(), name='game-list'),
    path('store/games/<int:pk>/', views.GameRetrieveAPIView.as_view(), name='game-detail'),
    path('store/games/trending/', views.GameTrendListAPIView.as_view(), name='game-trending-list'),
    path('store/games/trending/<int:pk>/', views.GameTrendRetrieveAPIView.as_view(), name='game-trending-detail'),

    # ==================== Most Sold URLs ====================
    path('store/products/most-sold/', views.MostSoldProductsListAPIView.as_view(), name='most-sold-products-list'),
    path('store/games/most-sold/', views.MostSoldGamesListAPIView.as_view(), name='most-sold-games-list'),

    # ==================== Banners ====================

    path('banners/', views.HomeBannerListView.as_view(), name='banner-list'),
    path('banners/create/', views.HomeBannerCreateView.as_view(), name='banner-create'),

    path('banners/<int:pk>/', views.HomeBannerDetailView.as_view(), name='banner-detail'),
    path('banners/<int:pk>/update/', views.HomeBannerUpdateView.as_view(), name='banner-update'),
    path('banners/<int:pk>/delete/', views.HomeBannerDeleteView.as_view(), name='banner-delete'),
]
