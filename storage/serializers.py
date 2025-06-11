from rest_framework import serializers

from storage.models import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['title', 'main_img', 'description', 'is_trend',
                  'is_deleted', 'created_at', 'updated_at']

    def validate(self, data):
        if data.get('is_trend', False):
            instance_pk = self.instance.pk if self.instance else None
            trending_count = Game.objects.filter(is_trend=True).exclude(pk=instance_pk).count()

            if trending_count >= 4:
                raise serializers.ValidationError(
                    {"is_trend": "Only 4 games can be marked as trending."}
                )
        return data
