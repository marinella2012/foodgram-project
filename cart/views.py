from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView

from cart.cart import Cart
from recipes.models import Recipe


class CartListView(ListView):
    template_name = 'cart_detail.html'

    def get_queryset(self):
        cart = Cart(self.request)
        recipes_id = cart.get_ids()
        return Recipe.objects.filter(pk__in=recipes_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список покупок'
        return context


def cart_remove(request, id):
    cart = Cart(request)
    if cart.in_cart(id):
        cart.remove(id)
    return redirect('cart_detail')


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
            string = (
                f'{ingredient["ingredients__name"]}-'
                f'{ingredient["amount"]} '
                f'{ingredient["ingredients__unit_of_measurement__name"]}; '
            )
            content += string + '\n'
    response = HttpResponse(content=content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
