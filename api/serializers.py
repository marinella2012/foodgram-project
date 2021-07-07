from rest_framework import serializers

from recipes.models import Ingredient
from users.models import User

from .models import Favorite


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CustomModelSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return self.Meta.model.objects.create(**validated_data)


class IngredientSerializer(serializers.ModelSerializer):
    unit_of_measurement = serializers.SlugRelatedField(read_only=True,
                                                       slug_field='name')

    class Meta:
        model = Ingredient
        fields = '__all__'


class FavoriteSerializer(CustomModelSerializer):
    class Meta:
        fields = ('recipe', )
        model = Favorite
