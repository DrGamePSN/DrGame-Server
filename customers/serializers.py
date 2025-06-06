# customers/serializers.py
from rest_framework import serializers
from .models import Customer, BusinessCustomer
from payments.models import Order, GameOrder, RepairOrder, Transaction


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.phone', max_length=11)

    class Meta:
        model = Customer
        fields = ['id', 'full_name', 'user', 'address', 'profile_pic', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']


class BusinessCustomerProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.phone', max_length=11)

    class Meta:
        model = BusinessCustomer
        fields = ['id', 'full_name', 'user', 'license', 'address', 'profile_pic', 'created_at', ]
        read_only_fields = ['id', 'created_at', 'user']


class BusinessCustomerUpgradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessCustomer
        fields = ['full_name', 'license', 'address', 'profile_pic']
        extra_kwargs = {
            'license': {'required': True}
        }

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        if BusinessCustomer.objects.filter(user=user).exists():
            raise serializers.ValidationError('You are already a business customer')
        if data['license'] is '' or data['license'] is None:
            raise serializers.ValidationError('Please provide a license as a business customer')
        if data['full_name'] is '' or data['full_name'] is None:
            raise serializers.ValidationError('Please type your name')
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        return BusinessCustomer.objects.create(user=user, **validated_data)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'order_type', 'amount', 'product', 'created_at']
        read_only_fields = ['id', 'created_at']


class GameOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameOrder
        fields = ['id', 'order_type', 'amount', 'product', 'games_count', 'selected_games_count', 'created_at']
        read_only_fields = ['id', 'created_at']


class RepairOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairOrder
        fields = ['id', 'order_type', 'amount', 'product', 'created_at']
        read_only_fields = ['id', 'created_at']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'transaction_type', 'amount', 'status', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']
