from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, validators

from .models import Cart

User = get_user_model()


class CartFavoriteMixin(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    id = serializers.CharField(source='recipe_id')

    def validate(self, attrs):
        if self.Meta.model.objects.filter(
            user=attrs.get('user'),
            recipe_id=attrs.get('recipe_id')
        ).exists():
            raise validators.ValidationError(_('Вы уже сделали это.'))
        return attrs


class CartSerializer(CartFavoriteMixin):
    class Meta:
        fields = ['id', 'user']
        model = Cart
