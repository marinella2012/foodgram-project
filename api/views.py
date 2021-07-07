from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response

from cart.cart import Cart
from recipes.models import Ingredient, Recipe
from users.models import User

from .models import Favorite
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, UserSerializer)

SUCCESS = {'success': True}
UNSUCCESS = {'success': False}


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        mask = self.request.query_params.get('query', '').lower()
        return Ingredient.objects.filter(name__icontains=mask)


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = Recipe.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    def get_object(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {
            self.lookup_field: self.kwargs[lookup_url_kwarg], **kwargs,
        }

        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)

        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object(user=self.request.user)
        success = instance.delete()
        return Response({'success': bool(success)}, status=status.HTTP_200_OK)


class PurchasesView(viewsets.ModelViewSet):
    def create(self, request):
        id = request.data.get('id')
        cart = Cart(self.request)
        if not Recipe.objects.filter(pk=id).exists() or cart.in_cart(id):
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=UNSUCCESS)
        cart.add(id)
        return Response(status=status.HTTP_201_CREATED, data=SUCCESS)

    def destroy(self, request, pk=None):
        cart = Cart(request)
        if Recipe.objects.filter(pk=pk).exists() and cart.in_cart(pk):
            cart.remove(pk)
            return Response(status=status.HTTP_202_ACCEPTED, data=SUCCESS)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=UNSUCCESS)


class FavoriteViewSet(CreateDestroyViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'recipe'
