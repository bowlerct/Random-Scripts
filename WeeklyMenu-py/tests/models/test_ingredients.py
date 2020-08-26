import pytest
from foodmenu.models import Ingredient

@pytest.mark.django_db()
def test_ingredient_name_field():
    ing = Ingredient.objects.create(name='carrots')
    field_label = ing._meta.get_field('name').verbose_name
    max_length = ing._meta.get_field('name').max_length
    assert field_label == 'name'
    assert max_length == 50

@pytest.mark.django_db()
def test_insert_ingredient(django_assert_num_queries):
    ingreds = ['carrots', 'broccolli', 'chicken broth', 'Ground Beef', 'Ribeye', 'NEW YORK STEAK STRIP']
    with django_assert_num_queries(6) as captured:
        for i in ingreds:
            Ingredient.objects.create(name=i)
    
    # Query total ingredients
    assert 'carrots' in captured.captured_queries[0]['sql']