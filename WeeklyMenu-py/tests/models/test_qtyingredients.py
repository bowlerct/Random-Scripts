import pytest
from foodmenu.models import QtyIngredient

def test_recipe_quantity_field(create_qtyingredient):
    rec, user = create_qtyingredient()
    field_label = rec._meta.get_field('quantity').verbose_name
    assert field_label == 'quantity'

def test_recipe_size_field(create_qtyingredient):
    rec, user = create_qtyingredient()
    field_label = rec._meta.get_field('size').verbose_name
    max_length = rec._meta.get_field('size').max_length
    assert field_label == 'size'
    assert max_length == 15