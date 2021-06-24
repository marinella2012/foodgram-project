import json

from django.db.models import Sum
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from recipes.models import Recipe

from .cart import Cart


@require_POST
def cart_add(request):
    recipe_id = json.loads(request.body).get('id')
    cart = Cart(request)
    recipe = get_object_or_404(Recipe, id=recipe_id)
    cart.add(recipe=recipe)
    if 'cart' not in request.META['HTTP_REFERER']:
        return JsonResponse({'success': True})
    return redirect('cart:cart_detail')


def cart_remove(request, recipe_id):
    cart = Cart(request)
    product = get_object_or_404(Recipe, id=recipe_id)
    cart.remove(product)
    if 'cart' not in request.META['HTTP_REFERER']:
        return JsonResponse({'success': True})
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})


def cart_download(request):
    cart = Cart(request)
    ids_recipes_in_purchase = [recipe['recipe'].pk for recipe in cart]
    recipes = Recipe.objects.filter(pk__in=ids_recipes_in_purchase).distinct()

    ingredients = recipes.order_by('ingredients__name').values(
        'ingredients__name',
        'ingredients__unit_of_measurement__name').annotate(
        amount=Sum('recipe_ingredient__quantity')).all()
    filename = 'cart-list.txt'
    content = ''
    for ingredient in ingredients:
        if ingredient["ingredients__name"] is not None:
            string = (f'{ingredient["ingredients__name"]}-'
                      f'{ingredient["amount"]} '
                      f'{ingredient["ingredients__unit_of_measurement__name"]}; ')
            content += string + '\n'
    response = HttpResponse(content=content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
