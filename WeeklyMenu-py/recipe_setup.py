

def newRecipe(name, book="", url="", recipeType="Dinner", owner=None):
    """
    Requires user already exists

    name: Name of Recipe
    mealType: [Breakfast, Lunch, Dinner]
    owner: username of owner

    returns id of recipe added or -1 if error occured
    """
    if not owner:
        print("[Error] owner not specified for recipe %" % name)
        return
    
    local_user = None
    try:
        local_user = User.objects.get(username='bowlerct')
    except User.DoesNotExist:
        local_user = User(first_name="Chris", last_name="Koerner", email='bowlerct@gmail.com', username='bowlerct')
        local_user.set_password("p@ssword1")
        local_user.save()

    print("Adding recipe {}".format(name))
    try:
        q = Recipe.objects.create(name=name, book=book, url=url, recipeType=recipeType, owner=local_user)
        return q.pk
    except Exception as e:
        print(e)
        return -1

def addIngredient(name, quantity, size, recipeId):
    """
    Adds an ingredient to a recipe. If ingredient does not exist
    it will be added

    name: Name of ingredient
    quantity: ingredient amount
    size: TSP, TBSP, CUP, PINT, QUART, GALLON, LITER, BUNCH, COUNT, POUND
    recipeId: database id of recipe
    """

    # lookup recipe
    r = None
    try:
        r = Recipe.objects.get(pk=recipeId)
    except Exception as e:
        # get throws exceptions if object does not exist or multiple entries were found
        print("[Error] unable to find recipe {}".format(recipeId))
        return
    
    # lookup or create ingredient
    qi, created = Ingredient.objects.get_or_create(name=name)
    
    # add ingredient
    print("Adding Ingredient {} to {}".format(name, recipeId))
    try:
        QtyIngredient.objects.create(name=qi, size=size, quantity=quantity, recipe=r)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    # This will run e.g. from python -i test.py, but will be skipped if from Django
    import django  # 1.7
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'menu.settings'
    django.setup()

    from foodmenu.models import Ingredient, Recipe, QtyIngredient
    from django.contrib.auth.models import User
    from django.db.models import Model
    import json

    owner="bowlerct"

    with open('init_recipes.json', 'r') as f:
        data = json.load(f)
        for rs in data['recipes']:
            rid = newRecipe(name=rs['name'], book=rs['book'], url=rs['url'], recipeType=rs['type'], owner=owner)
            for ig in rs['ingredients']:
                addIngredient(name=ig['name'], quantity=ig['quantity'], size=ig['size'], recipeId=rid)
