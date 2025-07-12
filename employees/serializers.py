from rest_framework import serializers

from accounts.models import CustomUser
from employees.models import EmployeeTask
from payments.models import GameOrder, Transaction, Order, RepairOrder, TransactionType
from storage.models import Game, SonyAccount, Product


class SoftDeleteSerializerMixin:
    def destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class EmployeeGameSerializer(SoftDeleteSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"
        read_only_fields = ['is_deleted', 'created_at', 'updated_at']


class EmployeeSonyAccountMatchedSerializer(SoftDeleteSerializerMixin, serializers.ModelSerializer):
    games = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')
    matching_games_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = SonyAccount
        fields = ['id', 'username', 'games', 'matching_games_count', 'region', 'created_at', 'updated_at']
        read_only_fields = ['is_deleted', 'created_at', 'updated_at']


class EmployeeSonyAccountSerializer(SoftDeleteSerializerMixin, serializers.ModelSerializer):
    employee = serializers.SerializerMethodField()
    games = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')

    class Meta:
        model = SonyAccount
        fields = "__all__"
        read_only_fields = ['is_deleted', 'created_at', 'updated_at']

    def get_employee(self, obj):
        if obj.employee:
            return f"{obj.employee.first_name} {obj.employee.last_name}"
        return None


class EmployeeTransactionSerializer(SoftDeleteSerializerMixin, serializers.ModelSerializer):
    transaction_type = serializers.SlugRelatedField(
        slug_field='title',
        queryset=TransactionType.objects.filter(is_deleted=False)
    )
    payer = serializers.SlugRelatedField(
        slug_field='phone',
        queryset=CustomUser.objects.all(),
        required=False,
        allow_null=True
    )
    receiver = serializers.SlugRelatedField(
        slug_field='phone',
        queryset=CustomUser.objects.all(),
        required=False,
        allow_null=True
    )
    payer_str = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    receiver_str = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'payer', 'payer_str', 'receiver', 'receiver_str', 'transaction_type', 'amount', 'status',
            'game_order', 'repair_order', 'course_order', 'order', 'description', 'is_deleted',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['is_deleted', 'created_at', 'updated_at']

    def validate(self, attrs):
        if attrs.get('payer') and attrs.get('payer_str'):
            raise serializers.ValidationError("فقط یکی از payer یا payer_str باید مقدار داشته باشد.")
        if attrs.get('receiver') and attrs.get('receiver_str'):
            raise serializers.ValidationError("فقط یکی از receiver یا receiver_str باید مقدار داشته باشد.")
        return attrs


class EmployeeProductSerializer(SoftDeleteSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ['is_deleted', 'created_at', 'updated_at', 'units_sold']


class EmployeeTaskSerializer(SoftDeleteSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = EmployeeTask
        fields = ['id', 'title', 'type', 'description', 'status', 'deadline', 'employee', 'created_at', 'updated_at']
        read_only_fields = ['employee', 'type', 'created_at', 'updated_at', 'is_deleted']

    def create(self, validated_data):
        employee = self.context['request'].user.employee
        validated_data['employee'] = employee
        validated_data['type'] = 'Personal'
        return super().create(validated_data)


class EmployeeProductOrderSerializer(SoftDeleteSerializerMixin, serializers.ModelSerializer):
    order_type = serializers.SlugRelatedField(read_only=True, slug_field='title')
    customer = serializers.SlugRelatedField(read_only=True, slug_field='full_name')

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ['is_deleted', 'created_at', 'updated_at']


class EmployeeGameOrderSerializer(SoftDeleteSerializerMixin, serializers.ModelSerializer):
    games = serializers.SlugRelatedField(slug_field='title', many=True, queryset=Game.objects.filter(is_deleted=False))

    class Meta:
        model = GameOrder
        fields = "__all__"
        read_only_fields = ['is_deleted', 'created_at', 'updated_at']


class EmployeeRepairOrderSerializer(SoftDeleteSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = RepairOrder
        fields = "__all__"
        read_only_fields = ['is_deleted', 'created_at', 'updated_at']
