from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .models import Recipe


def index(request):
    recipes = Recipe.objects.all()
    paginator = Paginator(recipes, settings.PAGINATION_PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
         request,
         'recipes/index.html',
         {'page': page, 'paginator': paginator}
    )
