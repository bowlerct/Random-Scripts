

def newIngredient(ing):
    print("Adding ingredient {}".format(ing))
    q = Ingredient(name=ing)
    try:
        q.save()
    except Exception as e:
        print(e)

def newRecipe(rec, mealType, usr):
    """
    Requires user already exists

    mealType = [Breakfast, Lunch, Dinner]
    """
    print("Adding recipe {}".format(rec))
    q = Recipe(name=rec, book=None, url=None, recipeType=mealType, owner=usr)
    try:
        q.save()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    # This will run e.g. from python -i test.py, but will be skipped if from Django
    import django  # 1.7
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'menu.settings'
    django.setup()

    from foodmenu.models import Ingredient, Recipe, QtyIngredient

    newIngreds = ['carrots','celery','broccolli','chicken broth']

    for entry in newIngreds:
        newIngredient(entry)

    # create admin user
    local_user = User.objects.filter(username='menuadmin')

    if local_user.count() == 1:
        local_user = local_user[0]
    else:
        local_user = User(first_name="Menu", last_name="Admin", email='', username='menuadmin')
        local_user.set_password("#####")
        local_user.save()
        print("Created admin {}".format(local_user.username))
