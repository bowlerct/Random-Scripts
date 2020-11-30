from django import forms
from django.forms.models import inlineformset_factory
from foodmenu.models import Recipe, QtyIngredient, RecipeMenu


class CreateRecipe(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    class Meta:
        model = Recipe
        fields = ['name', 'book', 'url', 'recipeType']


class EditRecipeForm(forms.ModelForm):
    class Meta:
        model = QtyIngredient
        fields = ['quantity', 'size', 'name']


IngredientsFormset = inlineformset_factory(Recipe, Recipe.ingredients.through, form=EditRecipeForm, extra=1)

class CreateMenu(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
    
    class Meta:
        model = RecipeMenu
        fields = ['date']
