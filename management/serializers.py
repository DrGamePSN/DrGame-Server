from rest_framework import serializers
from accounts.models import CustomUser
from customers.models import Customer, BusinessCustomer
from employees.models import Employee, Repairman, EmployeeRole
from payments.models import GameOrder, RepairOrder, Order, Transaction, TransactionType
from storage.models import SonyAccount, ProductCategory, Product, ProductCompany, ProductColor, ProductImage


# read serializers
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)  # اطلاعات کاربر مرتبط
    role = serializers.StringRelatedField()  # نمایش عنوان نقش
    income_type = serializers.CharField()  # نمایش نوع درآمد (مثل "پورسانت" یا "حقوق ثابت")

    class Meta:
        model = Employee
        fields = [
            'id',
            'user',
            'role',
            'profile_picture',
            'first_name',
            'last_name',
            'national_code',
            'employee_id',
            'balance',
            'income_type',
            'created_at',
            'updated_at'
        ]


class RepairmanSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)  # اطلاعات کاربر مرتبط

    class Meta:
        model = Repairman
        fields = [
            'id',
            'user',
            'profile_picture',
            'first_name',
            'last_name',
            'national_code',
            'balance',
            'created_at',
            'updated_at'
        ]


class EmployeeListSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True, source='employee_set')  # کارمندان مرتبط با نقش

    class Meta:
        model = EmployeeRole
        fields = [
            'id',
            'title',
            'description',
            'employees',
            'created_at',
            'updated_at'
        ]


class CustomerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)  # اطلاعات کاربر مرتبط

    class Meta:
        model = Customer
        fields = [
            'id',
            'full_name',
            'user',
            'address',
            'profile_pic',
            'is_deleted',
            'created_at',
            'updated_at'
        ]


class BusinessCustomerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)  # اطلاعات کاربر مرتبط

    class Meta:
        model = BusinessCustomer
        fields = [
            'id',
            'full_name',
            'user',
            'license',
            'address',
            'profile_pic',
            'is_deleted',
            'created_at',
            'updated_at'
        ]


class SonyAccountSerializer(serializers.ModelSerializer):
    games = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title',
    )
    status = serializers.StringRelatedField()
    bank_account = serializers.StringRelatedField()
    region = serializers.CharField()

    class Meta:
        model = SonyAccount
        fields = [
            'id',  # در صورت نیاز به ID
            'username',
            'password',
            'two_step',
            'status',
            'bank_account_status',
            'bank_account',
            'plus',
            'games',  # لیست نام بازی‌ها
            'region',
            'created_at',
            'updated_at'
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'img', 'created_at', 'updated_at']


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['id', 'title']


class ProductCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCompany
        fields = ['id', 'title']


class ProductSerializer(serializers.ModelSerializer):
    color = ProductColorSerializer()  # نمایش کامل اطلاعات رنگ
    company = ProductCompanySerializer()  # نمایش کامل اطلاعات برند
    images = ProductImageSerializer(many=True, read_only=True, source='productimage_set')  # تصاویر محصول
    category = serializers.StringRelatedField()  # نمایش عنوان دسته‌بندی

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'main_img',
            'description',
            'color',
            'category',
            'company',
            'price',
            'stock',
            'images',
            'created_at',
            'updated_at'
        ]


class ProductCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True, source='product_set')  # محصولات مرتبط با دسته‌بندی

    class Meta:
        model = ProductCategory
        fields = [
            'id',
            'title',
            'description',
            'img',
            'products',  # لیست محصولات در این دسته‌بندی
            'created_at',
            'updated_at'
        ]


class GameOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameOrder
        fields = ['id']  # فقط ID، در صورت نیاز می‌توانید فیلدهای بیشتری اضافه کنید


class RepairOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairOrder
        fields = ['id']  # فقط ID، در صورت نیاز می‌توانید فیلدهای بیشتری اضافه کنید


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    payer = CustomUserSerializer(read_only=True)  # اطلاعات پرداخت‌کننده
    receiver = CustomUserSerializer(read_only=True)  # اطلاعات دریافت‌کننده
    transaction_type = serializers.StringRelatedField()  # نمایش عنوان نوع تراکنش
    game_order = GameOrderSerializer(read_only=True)  # اطلاعات سفارش بازی
    repair_order = RepairOrderSerializer(read_only=True)  # اطلاعات سفارش تعمیر
    order = OrderSerializer(read_only=True)  # اطلاعات سفارش عمومی
    status = serializers.CharField()  # نمایش وضعیت به صورت رشته

    class Meta:
        model = Transaction
        fields = [
            'id',
            'payer',
            'receiver',
            'transaction_type',
            'amount',
            'status',
            'game_order',
            'repair_order',
            'order',
            'description',
            'created_at',
            'updated_at'
        ]


class TransactionTypeSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True, source='transaction_set')  # تراکنش‌های مرتبط

    class Meta:
        model = TransactionType
        fields = [
            'id',
            'title',
            'description',
            'transactions',  # لیست تراکنش‌های مرتبط
            'created_at',
            'updated_at'
        ]


# create serializers
class EmployeeRoleAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeRole
        fields = "__all__"


class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['phone', 'is_active', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'is_active': {'default': True},
            'is_staff': {'default': False},
            'is_superuser': {'default': False},
        }

    def create(self, validated_data):
        phone = validated_data.get('phone')
        user = CustomUser.objects.create_user(
            phone=phone,
            **{k: v for k, v in validated_data.items() if k not in ['phone']}
        )
        return user


class EmployeeCreateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True)  # فقط شماره تلفن دریافت می‌شود

    class Meta:
        model = Employee
        fields = [
            'phone', 'role', 'profile_picture', 'first_name', 'last_name',
            'national_code', 'employee_id', 'balance', 'income_type', 'is_deleted'
        ]
        extra_kwargs = {
            'is_deleted': {'default': False},
            'balance': {'default': 0.0},
        }

    def validate_phone(self, value):
        # اعتبارسنجی شماره تلفن
        if CustomUser.objects.filter(phone=value).exists():
            raise serializers.ValidationError("کاربری با این شماره تلفن قبلاً ثبت شده است.")
        if len(value) != 11 or not value.isdigit():
            raise serializers.ValidationError("شماره تلفن باید 11 رقم باشد.")
        return value

    def create(self, validated_data):
        # استخراج شماره تلفن و حذف آن از داده‌ها
        phone = validated_data.pop('phone')
        # ایجاد کاربر با شماره تلفن
        user = CustomUser.objects.create_user(phone=phone)
        user.save()
        # ایجاد کارمند با کاربر ساخته‌شده
        employee = Employee.objects.create(user=user, **validated_data)
        return employee


class SonyAccountAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = SonyAccount
        fields = ('username', 'password')


class ProductAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
