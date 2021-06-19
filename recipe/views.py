from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from api.models import Subscription
from foodgram.settings import PAGINATION_PAGE_SIZE

from .forms import RecipeForm
from .models import Recipe, Tag
from .utils import save_recipe

User = get_user_model()


def index(request):
    all_tags = Tag.objects.all()
    tags = request.GET.getlist('tag')
    filter_keys = {}
    if len(tags) != 0:
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
        return redirect('recipe_view', recipe_id=recipe.id, slug=recipe.slug)
    tags = Tag.objects.all()
    return render(
        request,
        'recipes/formRecipe.html',
        {'form': form, 'tags': tags}
    )


@login_required
def recipe_edit(request, slug, user_id):
    recipe = get_object_or_404(Recipe, slug=slug, author__pk=user_id)
    if request.user != recipe.author and not request.user.is_superuser:
        return redirect('index')
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None,
                      instance=recipe)
    tags = Tag.objects.all()
    if form.is_valid():
        author = recipe.author
        recipe = save_recipe(request, form, author, is_edit=True)
        return redirect('recipe_view', recipe_id=recipe.id, slug=recipe.slug)
    return render(request, 'recipes/formRecipe.html', {'form': form,
                                                       'recipe': recipe,
                                                       'tags': tags})


@login_required
def recipe_delete(request, slug, user_id):
    recipe = get_object_or_404(Recipe, slug=slug, author__pk=user_id)
    if request.user != recipe.author and not request.user.is_superuser:
        return redirect('index')
    recipe.delete()
    return redirect('index')


def profile_view(request, username, **filters):
    all_tags = Tag.objects.all()
    author = get_object_or_404(User, username=username)
    author_recipes = Recipe.objects.filter(author=author, **filters).distinct()
    is_followed = (
        request.user.is_authenticated
        and Subscription.objects.filter(
            user=request.user,
            author=author).exists())
    paginator = Paginator(author_recipes, PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'recipes/authorRecipe.html',
        {
            'is_followed': is_followed,
            'author': author,
            'page': page,
            'paginator': paginator,
            'all_tags': all_tags,
        }
    )
