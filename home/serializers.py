from rest_framework import serializers
from slugify import slugify

from .models import Cart, CartItem, BlogCategory, BlogPost, AboutUs, ContactUs, ContactSubmission, BlogTag
from storage.models import Product, ProductColor


# cart-item
class ProductColorCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['title']


class ProductCartItemSerializer(serializers.ModelSerializer):
    color = ProductColorCartItemSerializer()

    class Meta:
        model = Product
        fields = ['title', 'color', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductCartItemSerializer()
    total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'total', ]

    def get_total(self, obj):
        return obj.total_item_price


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

    def validate(self, data):
        product_item = data['product']
        product = Product.objects.get(pk=product_item.pk)
        if data['quantity'] > product.stock:
            raise serializers.ValidationError('out of stock!')
        return data

    def create(self, validated_data):
        cart_id = self.context['cart']
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        try:
            cart_item = CartItem.objects.get(product=product, cart_id=cart_id)
            current_quantity = cart_item.quantity
            if (current_quantity + quantity) > product.stock:
                raise serializers.ValidationError('out of stock!')
            else:
                cart_item.quantity += quantity
                cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart_id=cart_id, **validated_data)

        self.instance = cart_item
        return cart_item


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity', ]

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value

    def validate(self, data):
        cart_item = self.instance

        # Check product stock
        if 'quantity' in data and data['quantity'] > cart_item.product.stock:
            raise serializers.ValidationError({
                'quantity': f"Only {cart_item.product.stock} items available in stock"
            })
        return data


# cart

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'cart_items', 'total_price']
        read_only_fields = ['id', 'cart_items', 'total_price']

    def get_total_price(self, obj):
        return obj.total_price


class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id']
        read_only_fields = ['id']

    def create(self, validated_data):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return Cart.objects.create(user=request.user, **validated_data)
        else:
            if not request.session.session_key:
                request.session.create()
            return Cart.objects.create(session_key=request.session.session_key , **validated_data)


# blog
class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug', 'description', 'created_at']
        read_only_fields = ['slug', 'created_at']

    def create(self, validated_data):
        blog_category = BlogCategory(**validated_data)
        blog_category.slug = slugify(blog_category.name, allow_unicode=True)
        blog_category.save()
        return blog_category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.slug = slugify(instance.name, allow_unicode=True)
        instance.save()
        return instance


class PostBlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['name']


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'slug']

    def create(self, validated_data):
        blog_tag = BlogTag(**validated_data)
        blog_tag.slug = slugify(blog_tag.name, allow_unicode=True)
        blog_tag.save()
        return blog_tag

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.slug = slugify(instance.name, allow_unicode=True)
        instance.save()
        return instance


class BlogPostListSerializer(serializers.ModelSerializer):
    category = PostBlogCategorySerializer()
    tags = BlogTagSerializer(many=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'category', 'tags',
                  'featured_image', 'status', 'created_at', 'published_at'
                  ]
        read_only_fields = ['id', 'published_at', 'author', 'slug']


class BlogPostDetailSerializer(BlogPostListSerializer):
    class Meta(BlogPostListSerializer.Meta):
        fields = BlogPostListSerializer.Meta.fields + ['content', 'meta_description', 'updated_at']


class CreateBlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'author', 'category', 'tags', 'content', 'featured_image', 'meta_description',
                  'status', 'published_at', ]
        read_only_fields = ['id', 'published_at', 'author']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', None)
        blog_post = BlogPost(**validated_data)
        blog_post.slug = slugify(blog_post.title, allow_unicode=True)
        blog_post.author = self.context['user']
        blog_post.save()
        blog_post.tags.set(tags_data)

        return blog_post


class UpdateBlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'author', 'category', 'tags', 'content', 'featured_image', 'meta_description',
                  'status', 'published_at', ]
        read_only_fields = ['id', 'published_at', 'author']

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        if 'title' in validated_data:
            instance.slug = slugify(instance.title, allow_unicode=True)

        instance.save()

        if tags_data is not None:
            instance.tags.set(tags_data)

        return instance


# contact us & about us

class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ['id', 'title', 'subtitle', 'content', 'banner_image', 'team_image']
        read_only_fields = ['id']

        extra_kwargs = {
            'title': {'required': False},
            'subtitle': {'required': False},
            'content': {'required': False},
            'banner_image': {'required': False},
            'team_image': {'required': False},

        }


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['id', 'address', 'phone', 'email', 'map_embed_code', 'opening_hours', 'facebook_url', 'twitter_url',
                  'instagram_url']
        read_only_fields = ['id']

        extra_kwargs = {
            'address': {'required': False},
            'phone': {'required': False},
            'email': {'required': False},
            'map_embed_code': {'required': False},
            'opening_hours': {'required': False},
            'facebook_url': {'required': False},
            'twitter_url': {'required': False},
            'instagram_url': {'required': False},

        }


class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'user', 'email', 'subject', 'message', ]
        read_only_fields = ['user']

    def create(self, validated_data):
        user_id = self.context['user_id']
        return ContactSubmission.objects.create(user_id=user_id, **validated_data)
