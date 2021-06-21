from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, Tag, Measurement


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'measure')
    search_fields = ('title',)
    list_filter = ('title',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'image', 'description',
                    'pub_date', 'cook_time', 'slug')
    list_filter = ('author', )
    search_fields = ('title', 'author__username')
    autocomplete_fields = ('author', )
    ordering = ('-pub_date', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'quantity')
    search_fields = ('ingredient', 'recipe')

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
