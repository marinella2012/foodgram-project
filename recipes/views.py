from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from foodgram.settings import RECORDS_ON_THE_PAGE
from recipes.forms import RecipeForm
from recipes.models import Cart, Recipe, Tag, TagChoices
from recipes.utils import save_recipe
from users.models import User
from recipes.models import RecipeIngredient
from django.db.models import F, Sum
from django.http.response import HttpResponse
from .serializers import CartSerializer

TAGS = [TagChoices.BREAKFAST, TagChoices.LUNCH, TagChoices.DINNER]


def index(request):
    tags = request.GET.getlist('tags', TAGS)
    all_tags = Tag.objects.all()
    recipes = Recipe.objects.filter(tags__name__in=tags).distinct()
    if request.user.is_authenticated:
        recipes = recipes.annotate(
            in_cart=Exists(
                Cart.objects.filter(
                    user=request.user,
                    recipe_id=OuterRef('id')).only('id')
            )
        )
    paginator = Paginator(recipes, RECORDS_ON_THE_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'paginator': paginator,
        'page': page,
        'tags': tags,
        'all_tags': all_tags,
    }
    return render(request, 'index.html', context)


def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    context = {'recipe': recipe}
    return render(request, 'recipe.html', context)


@login_required
def create_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = save_recipe(request, form)
        return redirect(
            'recipe_detail',
            slug=recipe.slug
        )
    return render(request, 'form_recipe.html', {'form': form})


@login_required
def edit_recipe(request, slug, user_id):
    recipe = get_object_or_404(Recipe, slug=slug, author__pk=user_id)
    if request.user != recipe.author and not request.user.is_superuser:
        return redirect('index')
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None,
                      instance=recipe)
    if form.is_valid():
        author = recipe.author
        recipe = save_recipe(request, form, author, is_edit=True)
        return redirect(
            'recipe_detail',
            slug=recipe.slug
        )
    return render(request, 'form_recipe.html', {'form': form,
                                                'recipe': recipe})


@login_required
def recipe_delete(request, slug, user_id):
    recipe = get_object_or_404(Recipe, slug=slug, author__pk=user_id)
    if request.user != recipe.author and not request.user.is_superuser:
        return redirect('index')
    recipe.delete()
    return redirect('index')


def profile(request, username):
    tags = request.GET.getlist('tags', TAGS)
    all_tags = Tag.objects.all()
    author = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=author,
                                    tags__name__in=tags).distinct()
    paginator = Paginator(recipes, RECORDS_ON_THE_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'paginator': paginator,
        'page': page,
        'tags': tags,
        'all_tags': all_tags,
        'author': author
    }
    return render(request, 'profile.html', context)


@login_required
def favorites(request):
    tags = request.GET.getlist('tags', TAGS)
    all_tags = Tag.objects.all()
    recipes = Recipe.objects.filter(favorite_by__user=request.user,
                                    tags__name__in=tags).distinct()
    paginator = Paginator(recipes, RECORDS_ON_THE_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'paginator': paginator,
        'page': page,
        'tags': tags,
        'all_tags': all_tags,
    }
    return render(request, 'fav.html', context)


@login_required
def cart(request):
    user_cart = Recipe.objects.filter(shopping__user=request.user)
    return render(
        request,
        'cart_detail.html',
        context={'cart': user_cart}
    )


class CartViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
):
    serializer_class = CartSerializer

    queryset = Cart.objects.all()

    def get_object(self):
        return get_object_or_404(
            klass=self.queryset,
            user=self.request.user,
            recipe__id=self.kwargs.get('pk')
        )


@login_required
def cart_download(request):
    return HttpResponse(
        bytes('\r\n'.join(
            [
                (f"{ingredient['name']}: {ingredient['total']} "
                 f"{ingredient['unit']}")
                for ingredient in RecipeIngredient.objects.filter(
                    recipe__shopping__user=request.user
                ).values(
                    name=F('ingredient__name'),
                    unit=F('ingredient__unit__name')
                ).order_by(
                    'name'
                ).annotate(
                    total=Sum('amount')
                )
            ]
        ),
            'utf-8'
        ),
        headers={
            'Content-Type': 'text/plain',
            'Content-Disposition': 'attachment; filename="card_list.txt"'
        }
    )
