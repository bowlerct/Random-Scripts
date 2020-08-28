from django.db import models
from django.contrib.auth.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    book = models.CharField(max_length=100, verbose_name="Cookbook", blank=True)
    url = models.URLField(max_length=250, verbose_name="Link", blank=True)
    RECIPE_TYPE_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner')
    ]
    recipeType = models.CharField(
        max_length=15,
        choices=RECIPE_TYPE_CHOICES,
        verbose_name="Meal Type",
        default="Dinner",
        blank=False
    )
    ingredients = models.ManyToManyField(Ingredient, through='QtyIngredient', blank=True)
    # don't keep the recipe's if the user is removed
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class QtyIngredient(models.Model):
    name = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)  # 1, 1/4, 1/2, etc
    SIZE_TYPE_CHOICES = [
        ('TSP', 'Teaspoon'),
        ('TBSP', 'Tablespoon'),
        ('CUP', 'Cup'),
        ('PINT', 'Pint'),
        ('QUART', 'Quart'),
        ('GALLON', 'Gallon'),
        ('LITER', 'Liter'),
        ('BUNCH', 'Bunch')
    ]
    size = models.CharField(
        max_length=15,
        choices=SIZE_TYPE_CHOICES,
        default="TSP",
        blank=False
    )

    def __str__(self):
        return "{} {} {}".format(self.quantity, self.size, self.name)
