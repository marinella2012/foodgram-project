from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from foodgram.settings import PAGINATION_PAGE_SIZE

from .forms import RecipeForm
from .models import Recipe, Tag
from .utils import save_recipe

User = get_user_model()


def index(request):
    all_tags = Tag.objects.all()
    tags = request.GET.getlist('tag')
    filter_keys = {}
    if tags:
        filter_keys['tag__title__in'] = tags
    recipes = Recipe.objects.filter(**filter_keys).distinct()
    paginator = Paginator(recipes, PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'recipes/index.html',
        {
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'all_tags': all_tags,
        }
    )


def recipe_view_redirect(recipe_id):
    recipe = get_object_or_404(Recipe.objects.all(), id=recipe_id)
    return redirect('recipe_view', recipe_id=recipe.id, slug=recipe.slug)


def recipe_view(request, recipe_id, slug):
    recipe = get_object_or_404(
        Recipe.objects.select_related('author'),
        id=recipe_id,
        slug=slug
    )
    return render(request, 'recipes/singlePage.html', {'recipe': recipe})


@login_required
def recipe_new(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        recipe = save_recipe(request, form)
        print(recipe.slug)
        print(recipe.author.pk)
        return redirect('recipe_view', slug=recipe.slug,
                        user_id=recipe.author.pk)
    return render(request, 'recipes/formRecipe.html', {'form': form})


def profile_view(request):
    tags = request.GET.getlist('tag')
    all_tags = Tag.objects.all()
    filter_keys = {}
    if tags:
        filter_keys['tag__title__in'] = tags
    recipes = Recipe.objects.filter(**filter_keys).distinct()
    paginator = Paginator(recipes, PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'recipes/authorRecipe.html',
        {
            'page': page,
            'paginator': paginator,
            'tags': tags,
            'all_tags': all_tags,
        }
    )
