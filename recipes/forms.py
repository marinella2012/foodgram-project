from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        exclude = ['pub_date', 'slug', 'author', 'ingredients']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
