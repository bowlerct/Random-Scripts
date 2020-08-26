import pytest
from foodmenu.forms import CreateRecipe

# ensure form fields have correct labels
@pytest.mark.parametrize("field",[('name','Name'),('book','Cookbook'),('url','Link'),('recipeType','Meal Type')])
def test_createform_check_fields(field):
    form = CreateRecipe()
    name, verbose = field
    f = form.fields[name]
    assert f.label == verbose
