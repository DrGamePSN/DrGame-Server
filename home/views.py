from unicodedata import category

from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from storage.models import Game
from storage.serializers import GameSerializer
from .serializers import CartSerializer, AddCartItemSerializer, UpdateCartItemSerializer, CartItemSerializer, \
    CartCreateSerializer, BlogCategorySerializer, UpdateBlogPostSerializer, \
    CreateBlogPostSerializer, AboutUsSerializer, ContactUsSerializer, ContactSubmissionSerializer, BlogTagSerializer, \
    BlogPostDetailSerializer, BlogPostListSerializer, CourseRetrieveSerializer, \
    CourseListCreateSerializer, CourseUpdateSerializer, VideoSerializer, VideoCreateSerializer, VideoUpdateSerializer, \
    CourseOrderSerializer, CourseOrderForAdminSerializer, CourseOrderCreateSerializer, CourseOrderUpdateSerializer
from .models import Cart, CartItem, BlogCategory, BlogPost, AboutUs, ContactUs, ContactSubmission, BlogTag, Course, \
    Video, CourseOrder


# trending games

class GameTrendListAPIView(generics.ListAPIView):
    serializer_class = GameSerializer
    queryset = Game.objects.filter(is_trend=True).all()

class GameTrendRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = GameSerializer
    queryset = Game.objects.filter(is_trend=True).all()

# cart
class CartDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.filter(is_deleted=False).prefetch_related('cart_items__product__color').all()
    lookup_field = 'id'


class CartCreateAPIView(generics.CreateAPIView):
    serializer_class = CartCreateSerializer
    queryset = Cart.objects.filter(is_deleted=False).all()


class CartDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.filter(is_deleted=False).all()
    lookup_field = 'id'


# cart-item

class CartItemListAPIView(generics.ListAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        cart = self.kwargs.get('id')
        return (CartItem.objects.select_related('product__color', 'product__company', 'cart').filter(cart=cart,
                                                                                                     is_deleted=False))


class CartItemDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        cart = self.kwargs.get('id')
        return (CartItem.objects.select_related('product__color', 'product__company', 'cart').filter(cart=cart,
                                                                                                     is_deleted=False))


class CartItemAddCreateAPIView(generics.CreateAPIView):
    serializer_class = AddCartItemSerializer

    def get_queryset(self):
        cart = self.kwargs.get('id')
        return (CartItem.objects.select_related('product__color', 'product__company', 'cart').filter(cart=cart,
                                                                                                     is_deleted=False))

    def get_serializer_context(self):
        return {'cart': self.kwargs.get('id')}

    def post(self, request, *args, **kwargs):
        cart = self.kwargs.get('id')
        created_serializer = self.serializer_class(data=request.data, context={'cart': cart})
        created_serializer.is_valid(raise_exception=True)
        created_item = created_serializer.save()
        serializer = CartItemSerializer(created_item)
        return Response(serializer.data)


class CartItemUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UpdateCartItemSerializer

    def get_queryset(self):
        cart = self.kwargs.get('id')
        return (CartItem.objects.select_related('product__color', 'product__company', 'cart').filter(cart=cart,
                                                                                                     is_deleted=False))

    def get_serializer_context(self):
        return {'item_id': self.kwargs.get('pk')}

    def put(self, request, *args, **kwargs):
        cart = self.kwargs.get('id')
        pk = self.kwargs.get('pk')
        try:
            cart_item = CartItem.objects.get(cart=cart, pk=pk)
            updated_serializer = self.serializer_class(cart_item, data=request.data)
            updated_serializer.is_valid(raise_exception=True)
            updated_item = updated_serializer.save()
            serializer = CartItemSerializer(updated_item)
            return Response(serializer.data)

        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CartItemDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        cart = self.kwargs.get('id')
        return (CartItem.objects.select_related('product__color', 'product__company', 'cart').filter(cart=cart,
                                                                                                     is_deleted=False))

    def delete(self, request, *args, **kwargs):
        cart = self.kwargs.get('id')
        pk = self.kwargs.get('pk')
        try:
            cart_item = CartItem.objects.get(cart=cart, pk=pk)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# blog-category

class BlogCategoryListAPIView(generics.ListAPIView):
    queryset = BlogCategory.objects.filter(is_deleted=False).all()
    serializer_class = BlogCategorySerializer
    filter_backends = [SearchFilter, ]
    search_fields = ['title']


class BlogCategoryCreateAPIView(generics.CreateAPIView):
    queryset = BlogCategory.objects.filter(is_deleted=False).all()
    serializer_class = BlogCategorySerializer


class BlogCategoryUpdateAPIView(generics.UpdateAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    lookup_field = 'slug'


class BlogCategoryDeleteAPIView(generics.DestroyAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    lookup_field = 'slug'


# blog tag

class BlogTagListAPIView(generics.ListAPIView):
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer


class BlogTagCreateAPIView(generics.CreateAPIView):
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer


class BlogTagUpdateAPIView(generics.UpdateAPIView):
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer
    lookup_field = 'slug'


class BlogTagDeleteAPIView(generics.DestroyAPIView):
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer
    lookup_field = 'slug'


# blog-post

class BlogPostListAPIView(generics.ListAPIView):
    queryset = BlogPost.objects.select_related('category', 'author').prefetch_related('tags').filter(
        status='published').all()
    serializer_class = BlogPostListSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title']
    filterset_fields = ['category']
    ordering_fields = ['created_at']


class BlogPostRetrieveAPIView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.select_related('category', 'author').prefetch_related('tags').filter(
        status='published').all()
    serializer_class = BlogPostDetailSerializer
    lookup_field = 'slug'


class BlogPostCreateAPIView(generics.CreateAPIView):
    queryset = BlogPost.objects.select_related('category', 'author').prefetch_related('tags').filter(
        status='published').all()
    serializer_class = CreateBlogPostSerializer

    def post(self, request, *args, **kwargs):
        created_serializer = self.serializer_class(data=request.data, context={'user': self.request.user})
        created_serializer.is_valid(raise_exception=True)
        created_item = created_serializer.save()
        serializer = BlogPostDetailSerializer(created_item)
        return Response(serializer.data)


class BlogPostUpdateAPIView(generics.UpdateAPIView):
    queryset = BlogPost.objects.select_related('category', 'author').prefetch_related('tags').all()
    serializer_class = UpdateBlogPostSerializer
    lookup_field = 'slug'

    # http_method_names = ['patch']
    def put(self, request, *args, **kwargs):
        post_slug = self.kwargs.get('slug')
        post = BlogPost.objects.get(slug=post_slug)
        updated_serializer = self.serializer_class(post, data=request.data)
        updated_serializer.is_valid(raise_exception=True)
        updated_item = updated_serializer.save()
        serializer = BlogPostDetailSerializer(updated_item)
        return Response(serializer.data)


class BlogPostDeleteAPIView(generics.DestroyAPIView):
    queryset = BlogPost.objects.select_related('category', 'author').prefetch_related('tags').all()
    serializer_class = BlogPostDetailSerializer
    lookup_field = 'slug'


# nested urls for blog posts & categories => blog/categories/2/posts

class BlogPostListByCategoryAPIView(generics.ListAPIView):
    serializer_class = BlogPostListSerializer

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created_at']

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        return BlogPost.objects.filter(
            category__slug=category_slug,
            status='published'
        ).select_related('category', 'author').prefetch_related('tags').order_by('-created_at')


# nested urls for blog posts & categories => blog/categories/2/posts/3

class BlogPostRetrieveByCategoryAPIView(generics.RetrieveAPIView):
    serializer_class = BlogPostDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        return BlogPost.objects.filter(
            category__slug=category_slug,
            status='published'
        ).select_related('category', 'author').prefetch_related('tags').order_by('-created_at')


# contact us & about us

class AboutUsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = AboutUsSerializer

    def get_object(self):
        obj = get_object_or_404(AboutUs.objects.filter(is_deleted=False))
        return obj


class AboutUsCreateAPIView(generics.CreateAPIView):
    serializer_class = AboutUsSerializer

    queryset = AboutUs.objects.all()

    def create(self, request, *args, **kwargs):
        if AboutUs.objects.count() >= 1:
            return Response(
                {'error': 'Only one AboutUs entry allowed. Please delete existing entries first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)


class AboutUsDeleteAPIView(generics.DestroyAPIView):
    serializer_class = AboutUsSerializer

    def get_object(self):
        obj = get_object_or_404(AboutUs.objects.filter(is_deleted=False))
        return obj


class AboutUsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = AboutUsSerializer
    http_method_names = ['put']

    def get_object(self):
        obj = get_object_or_404(AboutUs.objects.filter(is_deleted=False))
        return obj


class ContactUsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ContactUsSerializer

    def get_object(self):
        obj = get_object_or_404(ContactUs.objects.filter(is_deleted=False))
        return obj


class ContactUsCreateAPIView(generics.CreateAPIView):
    serializer_class = ContactUsSerializer
    queryset = ContactUs.objects.all()

    def create(self, request, *args, **kwargs):
        if ContactUs.objects.count() >= 1:
            return Response(
                {'error': 'Only one ContactUs entry allowed. Please delete existing entries first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)


class ContactUsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ContactUsSerializer
    http_method_names = ['put']

    def get_object(self):
        obj = get_object_or_404(ContactUs.objects.filter(is_deleted=False))
        return obj


class ContactUsDeleteAPIView(generics.DestroyAPIView):
    serializer_class = ContactUsSerializer

    def get_object(self):
        obj = get_object_or_404(ContactUs.objects.filter(is_deleted=False))
        return obj


class ContactSubmissionCreateAPIView(generics.CreateAPIView):
    serializer_class = ContactSubmissionSerializer
    queryset = ContactSubmission.objects.select_related('user').all()

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


# Video Course

class CourseListAPIView(generics.ListAPIView):
    serializer_class = CourseListCreateSerializer
    queryset = Course.objects.filter(status='published').prefetch_related('videos').all()


class CourseRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CourseRetrieveSerializer
    queryset = Course.objects.filter(status='published').prefetch_related(Prefetch(
        'videos',
        queryset=Video.objects.filter(status='published').order_by('priority')
    )).all()
    lookup_field = 'slug'


class CourseCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseListCreateSerializer
    queryset = Course.objects.all()


class CourseUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CourseUpdateSerializer
    queryset = Course.objects.all()
    lookup_field = 'slug'


class CourseDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CourseListCreateSerializer
    queryset = Course.objects.all()
    lookup_field = 'slug'


# Video

class VideoListAPIView(generics.ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        course_slug = self.kwargs.get('course_slug')
        return Video.objects.filter(course__slug=course_slug, status='published').select_related('course').order_by(
            'priority').all()


class VideoRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = VideoSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        course_slug = self.kwargs.get('course_slug')
        return Video.objects.filter(course__slug=course_slug, status='published').select_related('course').order_by(
            'priority').all()


class VideoCreateAPIView(generics.CreateAPIView):
    serializer_class = VideoCreateSerializer

    def get_queryset(self):
        course_slug = self.kwargs.get('course_slug')
        return Video.objects.select_related('course').filter(course__slug=course_slug).all()

    def get_serializer_context(self):
        course_slug = self.kwargs.get('course_slug')
        return {'course': Course.objects.get(slug=course_slug)}


class VideoUpdateAPIView(generics.UpdateAPIView):
    serializer_class = VideoUpdateSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        course_slug = self.kwargs.get('course_slug')
        return Video.objects.select_related('course').filter(course__slug=course_slug).all()


class VideoDeleteAPIView(generics.DestroyAPIView):
    serializer_class = VideoSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        course_slug = self.kwargs.get('course_slug')
        return Video.objects.select_related('course').filter(course__slug=course_slug).all()


# Course Order

class CourseOrderListAPIView(generics.ListAPIView):

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return CourseOrderForAdminSerializer
        return CourseOrderSerializer

    def get_queryset(self):
        return CourseOrder.objects.select_related('course', 'user').filter(user=self.request.user).all()


class CourseOrderRetrieveAPIView(generics.RetrieveAPIView):

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return CourseOrderForAdminSerializer
        return CourseOrderSerializer

    def get_queryset(self):
        return CourseOrder.objects.select_related('course', 'user').filter(user=self.request.user).all()


class CourseOrderCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseOrderCreateSerializer

    def get_queryset(self):
        return CourseOrder.objects.select_related('course', 'user').filter(user=self.request.user).all()


class CourseOrderUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CourseOrderUpdateSerializer

    def get_queryset(self):
        return CourseOrder.objects.select_related('course', 'user').filter(user=self.request.user).all()


class CourseOrderDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CourseOrderSerializer

    def get_queryset(self):
        return CourseOrder.objects.select_related('course', 'user').filter(user=self.request.user).all()
