from unicodedata import category

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import CartSerializer, AddCartItemSerializer, UpdateCartItemSerializer, CartItemSerializer, \
    CartCreateSerializer, BlogCategorySerializer, BlogPostSerializer, UpdateBlogPostSerializer, \
    CreateBlogPostSerializer, AboutUsSerializer, ContactUsSerializer, ContactSubmissionSerializer
from .models import Cart, CartItem, BlogCategory, BlogPost, AboutUs, ContactUs, ContactSubmission


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
        return (CartItem.objects.select_related('product__color', 'cart').
                filter(cart=cart, is_deleted=False).all())


class CartItemDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        cart = self.kwargs.get('id')
        return (CartItem.objects.select_related('product__color', 'cart').
                filter(cart=cart, is_deleted=False).all())


class CartItemAddCreateAPIView(generics.CreateAPIView):
    serializer_class = AddCartItemSerializer

    # queryset = CartItem.objects.select_related('product__color', 'cart').filter(is_deleted=False).all()
    def get_queryset(self):
        cart = self.kwargs.get('id')
        return (CartItem.objects.select_related('product__color', 'cart').
                filter(cart=cart, is_deleted=False).all())

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
        return (CartItem.objects.select_related('product__color', 'cart').
                filter(cart=cart, is_deleted=False).all())

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
        return (CartItem.objects.select_related('product__color', 'cart').
                filter(cart=cart, is_deleted=False).all())

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
    permission_classes = [IsAdminUser]


class BlogCategoryUpdateAPIView(generics.UpdateAPIView):
    queryset = BlogCategory.objects.filter(is_deleted=False).all()
    serializer_class = BlogCategorySerializer
    permission_classes = [IsAdminUser]


class BlogCategoryDeleteAPIView(generics.DestroyAPIView):
    queryset = BlogCategory.objects.filter(is_deleted=False).all()
    serializer_class = BlogCategorySerializer
    permission_classes = [IsAdminUser]


# blog-post

class BlogPostListAPIView(generics.ListAPIView):
    queryset = BlogPost.objects.select_related('category').filter(is_deleted=False).all()
    serializer_class = BlogPostSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title']
    filterset_fields = ['category']
    ordering_fields = ['created_at']


class BlogPostRetrieveAPIView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.select_related('category').filter(is_deleted=False).all()
    serializer_class = BlogPostSerializer


class BlogPostCreateAPIView(generics.CreateAPIView):
    queryset = BlogPost.objects.select_related('category').filter(is_deleted=False).all()
    serializer_class = CreateBlogPostSerializer
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        created_serializer = self.serializer_class(data=request.data)
        created_serializer.is_valid(raise_exception=True)
        created_item = created_serializer.save()
        serializer = BlogPostSerializer(created_item)
        return Response(serializer.data)


class BlogPostUpdateAPIView(generics.UpdateAPIView):
    queryset = BlogPost.objects.select_related('category').filter(is_deleted=False).all()
    serializer_class = UpdateBlogPostSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        post_pk = self.kwargs.get('pk')
        post = BlogPost.objects.get(pk=post_pk)
        updated_serializer = self.serializer_class(post, data=request.data)
        updated_serializer.is_valid(raise_exception=True)
        updated_item = updated_serializer.save()
        serializer = BlogPostSerializer(updated_item)
        return Response(serializer.data)


class BlogPostDeleteAPIView(generics.DestroyAPIView):
    queryset = BlogPost.objects.select_related('category').filter(is_deleted=False).all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAdminUser]


# nested urls for blog posts & categories => blog/categories/2/posts

class BlogPostListByCategoryAPIView(generics.ListAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created_at']

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return BlogPost.objects.filter(
            category_id=category_id,
            is_deleted=False
        ).select_related('category').order_by('-created_at')


# nested urls for blog posts & categories => blog/categories/2/posts/3

class BlogPostRetrieveByCategoryAPIView(generics.RetrieveAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return BlogPost.objects.filter(
            category_id=category_id,
            is_deleted=False
        ).select_related('category').order_by('-created_at')


# contact us & about us

class AboutUsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = AboutUsSerializer

    def get_object(self):
        obj = get_object_or_404(AboutUs.objects.filter(is_deleted=False))
        return obj


class AboutUsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = AboutUsSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['put']

    def get_object(self):
        obj = get_object_or_404(AboutUs.objects.filter(is_deleted=False))
        return obj


class ContactUsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ContactUsSerializer

    def get_object(self):
        obj = get_object_or_404(ContactUs.objects.filter(is_deleted=False))
        return obj


class ContactSubmissionCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSubmissionSerializer
    queryset = ContactSubmission.objects.select_related('user').all()

    def get_serializer_context(self):
        return {'user_id' : self.request.user.id}

