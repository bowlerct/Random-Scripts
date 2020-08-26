import pytest
from foodmenu.models import Ingredient, Recipe, QtyIngredient

@pytest.fixture
def create_recipe(db, create_user, test_password):
    def make_recipe(user=None, recipe_name="Stew", **kwargs):
        if user is None:
            user = create_user(**kwargs)
        return Recipe(name=recipe_name, owner=user, book="Home", url="http://test.com/stew"), user
    return make_recipe

@pytest.fixture
def create_qtyingredient(db, create_recipe):
    def make_qtyingredient(**kwargs):
        ing = Ingredient.objects.create(name="carrots")
        recipe, user = create_recipe()
        qty = QtyIngredient(name=ing, size="TSP", quantity=1, recipe=recipe)
        return qty, user
    return make_qtyingredient
