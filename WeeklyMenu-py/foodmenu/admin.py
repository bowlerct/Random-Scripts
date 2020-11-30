from django.contrib import admin

# Register your models here.

from .models import Ingredient, QtyIngredient, Recipe, RecipeMenu

admin.site.register(Ingredient)
admin.site.register(QtyIngredient)
admin.site.register(Recipe)
admin.site.register(RecipeMenu)
