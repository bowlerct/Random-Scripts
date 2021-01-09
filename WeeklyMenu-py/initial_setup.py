

def newIngredient(ing):
    print("Adding ingredient {}".format(ing))
    try:
        Ingredient.ojbects.create(name=ing)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    # This will run e.g. from python -i test.py, but will be skipped if from Django
    import django  # 1.7
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'menu.settings'
    django.setup()

    from django.contrib.auth.models import User
    from foodmenu.models import Ingredient, Recipe, QtyIngredient

    newIngreds = [
        'carrots','celery','broccolli','chicken broth'
        ]

    for entry in newIngreds:
        newIngredient(entry)

    # create admin user
    local_user = User.objects.filter(username='menuadmin')

    if local_user.count() == 1:
        local_user = local_user[0]
    else:
        local_usefoodmenu/models.pyr = User(first_name="Menu", last_name="Admin", email='', username='menuadmin')
        local_user.set_password("p@ssword1")
        local_user.save()
        print("Created admin {}".format(local_user.username))
