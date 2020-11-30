

def newRecipe(name, book="", url="", recipeType="Dinner", owner=None):
    """
    Requires user already exists

    mealType = [Breakfast, Lunch, Dinner]
    """
    if not owner:
        print("[Error] owner not specified for recipe %" % name)
        return
    
    local_user = User.objects.filter(username='bowlerct')

    if local_user.count() == 1:
        local_user = local_user[0]
    else:
        local_user = User(first_name="Chris", last_name="Koerner", email='bowlerct@gmail.com', username='bowlerct')
        local_user.set_password("#####")
        local_user.save()

    print("Adding recipe {}".format(name))
    q = Recipe(name=name, book=book, url=url, recipeType=recipeType, owner=local_user)
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
    from django.contrib.auth.models import User

    # Breakfast
    newRecipe(name='Keto Toast', book="", url='https://ketosummit.com/quick-keto-toast-recipe/', recipeType="Breakfast", owner='bowlerct')
    newRecipe(name='Sausage Egg Cheese Bites', book="", url='https://www.maebells.com/sausage-egg-and-cheese-bites-low-carb-keto/', recipeType="Breakfast", owner='bowlerct')
    newRecipe(name='Zucchini Muffins', book="", url='https://blog.bulletproof.com/zucchini-muffins-recipe-keto-paleo-3c/', recipeType="Breakfast", owner='bowlerct')
    newRecipe(name='Sausage Spinach Quiche', book="", url='https://www.homemadeinterest.com/sausage-and-spinach-crustless-quiche-low-carb-keto/', recipeType="Breakfast", owner='bowlerct')
    # newRecipe(name='', book="", url='', recipeType="Breakfast", owner='bowlerct')

    # Lunch
    # newRecipe(name='Beef Stew', book="", url='', recipeType="Lunch", owner='bowlerct')

    # Dinner
    newRecipe(name='Thai Sweet Potato noodles', book="", url='https://www.cookinglight.com/recipes/thai-sweet-potato-noodle-bowls', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Keto Pizza', book="", url='https://www.dietdoctor.com/recipes/keto-pizza', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Lamb Burgers With Pistachio', book="", url='https://thrivemarket.com/blog/lamb-burgers-with-pistachio-pesto', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Lamb Curry', book="", url='https://www.thespruceeats.com/rogan-josh-recipe-1957574', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Pomegranate Flank Steak', book="", url='https://www.runningtothekitchen.com/pomegranate-flank-steak/', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Chimichurri Flank Steak', book="", url='https://www.carbmanager.com/recipe/keto-chimichurri-flank-steak', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Pot Roast', book="", url='https://www.tasteofhome.com/recipes/ultimate-pot-roast/', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Taco Salad', book="", url='https://www.lowcarbmaven.com/healthy-low-carb-taco-salad/', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Turkey Feta Meatballs', book="", url='https://www.ibreatheimhungry.com/sun-dried-tomato-feta-meatballs-low-carb-gluten-free/', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Turkey Kale Rice Soup', book="", url='https://www.foodnetwork.com/recipes/giada-de-laurentiis/turkey-kale-and-brown-rice-soup-recipe-2041444', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Turkey Curry', book="", url='https://www.evolvingtable.com/ground-turkey-curry/#wprm-recipe-container-4967', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Chicken Sun Dried Tomato', book="", url='https://www.savorytooth.com/sun-dried-tomato-chicken/', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Peso Chicken Casserole', book="", url='https://www.dietdoctor.com/recipes/keto-pesto-chicken-casserole', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Bacon Ranch Chicken Casserole', book="", url='https://www.wholesomeyum.com/recipes/chicken-bacon-ranch-casserole-recipe-easy-low-carb/', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Balsamic Chicken Thighs', book="", url='https://www.sugarfreemom.com/recipes/crock-pot-balsamic-chicken-thighs/', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Lemon Garlic Chicken Thighs', book="", url='https://www.eatwell101.com/lemon-garlic-butter-thighs-and-green-beans-skillet', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Buffalo Shrimp Wraps', book="", url='https://www.delish.com/cooking/a26331032/buffalo-shrimp-lettuce-wraps-recipe/', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Shrimp Scampi', book="", url='https://ketogasm.com/keto-shrimp-scampi-recipe/', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Cauliflower Mac and Cheese', book="", url='https://www.wholesomeyum.com/recipes/cauliflower-mac-and-cheese-recipe-low-carb-keto-gluten-free/#pinit', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Better Keto Pizza', book="", url='https://www.thedietchefs.com/keto-pizza-10-minutes-better-fathead-crust-keto-pizza/', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Sausage Cabbage', book="", url='https://www.lowcarbmaven.com/super-easy-sausage-cabbage-dinner/', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Jalapeno Poppers', book="", url='https://www.wholesomeyum.com/recipes/cream-cheese-jalapeno-poppers-with-bacon-low-carb-gluten-free/#pinit', recipeType="Dinner", owner='bowlerct')
    # Sides but under Dinner
    newRecipe(name='Cool Ranch Zucchini', book="", url='https://www.delish.com/cooking/recipe-ideas/a22344312/cool-ranch-zucchini-chips/', recipeType="Dinner", owner='bowlerct')
    newRecipe(name='Creamy Broccoli', book="", url='https://gimmedelicious.com/creamy-broccoli/#wprm-recipe-container-14264', recipeType="Dinner", owner='bowlerct')
    # newRecipe(name='', book="", url='', recipeType="Dinner", owner='bowlerct')
