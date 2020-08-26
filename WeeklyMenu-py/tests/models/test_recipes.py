import pytest
from foodmenu.models import Ingredient, Recipe, QtyIngredient

@pytest.mark.parametrize("field",[('name','name',100),('book','Cookbook', 100),('url','Link', 250)])
def test_recipe_fields(field, create_recipe):
    rec, user = create_recipe()
    name, verbose, length = field
    field_label = rec._meta.get_field(name).verbose_name
    max_length = rec._meta.get_field(name).max_length
    assert field_label == verbose
    assert max_length == length

@pytest.mark.django_db()
def test_insert_recipe(create_user, test_password):
    user = create_user()
    ing = Ingredient.objects.create(name='carrots')
    stew = Recipe.objects.create(name='Beef Stew', book='Home', url='http://foo.com/beefstew', owner=user)
    qtying = QtyIngredient.objects.create(name=ing, quantity=1, size='TSP', recipe=stew)
    assert qtying is not None