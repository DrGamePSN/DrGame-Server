from rest_framework import serializers

from payments.models import GameOrder


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameOrder
        fields = '__all__'

