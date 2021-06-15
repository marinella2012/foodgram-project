from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'title',
            'tag',
            'cook_time',
            'description',
            'image',
        )
        widgets = {
            'tags': forms.CheckboxSelectMultiple()
#                attrs={'class': 'tags__checkbox'}
#            ),
        }
