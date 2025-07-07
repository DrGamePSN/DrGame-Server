from rest_framework import serializers

from payments.models import GameOrder
from storage.models import Game, SonyAccount


class EmployeeGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"


class GameOrderSerializer(serializers.ModelSerializer):
    games = EmployeeGameSerializer(many=True, read_only=True)

    class Meta:
        model = GameOrder
        fields = (
            "customer", "account_setter", "data_uploader", "order_type", "amount", "product", "games", "games_count",
            "selected_games_count", "status", "created_at")


class EmployeeSonyAccountSerializer(serializers.ModelSerializer):
    games = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')
    matching_games_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = SonyAccount
        fields = ['id', 'username', 'games', 'matching_games_count', 'region', 'created_at', 'updated_at']
