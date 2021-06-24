from decimal import Decimal

from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from recipes.models import Ingredient, RecipeIngredient


def get_ingredients(request):
<<<<<<< HEAD:recipe/utils.py
    ingredients = {}
    for key, title in request.POST.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            ingredients[title] = request.POST[f'valueIngredient_{num}']
    return ingredients
=======
    result = {}
    for key, value in request.POST.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            result[value] = request.POST[f'valueIngredient_{num}']
    return result
>>>>>>> new:recipes/utils.py


def save_recipe(request, form, author=None, is_edit=False):
    try:
        print(form)
        recipe = form.save(commit=False)
        recipe.author = author if author else request.user
        recipe.save()

        if is_edit:
            tmp_ingredients = RecipeIngredient.objects.filter(
                recipe=recipe).delete()
        with transaction.atomic():
            ingredients = get_ingredients(request)
            recipe_ingredients = []
<<<<<<< HEAD:recipe/utils.py
            for title, quantity in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=title)
=======
            for name, quantity in ingredients.items():
                ingredient = get_object_or_404(Ingredient, name=name)
>>>>>>> new:recipes/utils.py
                obj = RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=abs(Decimal(quantity.replace(',', '.')))
                )
                recipe_ingredients.append(obj)
            RecipeIngredient.objects.bulk_create(recipe_ingredients)
            form.save_m2m()
            return recipe
    except IntegrityError:
        if is_edit:
            RecipeIngredient.objects.bulk_create(tmp_ingredients)
        return HttpResponseBadRequest
<<<<<<< HEAD:recipe/utils.py


def edit_recipe(request, form, instance):
    try:
        with transaction.atomic():
            RecipeIngredient.objects.filter(recipe=instance).delete()
            return save_recipe(request, form)
    except IntegrityError:
        raise


def generate_pdf(template_name, context):
    pdf_options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
    }
    html = get_template(template_name).render(context)
    return pdfkit.from_string(html, False, options=pdf_options)
=======
>>>>>>> new:recipes/utils.py
