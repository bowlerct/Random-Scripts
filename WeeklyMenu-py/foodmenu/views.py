from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from django.core.exceptions import PermissionDenied
from foodmenu.models import Recipe, RecipeMenu
from foodmenu.forms import CreateRecipe, IngredientsFormset
import datetime
import random
import json

# authentication
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    today = datetime.datetime.now().date()
    return render(request, "home.tmpl", {"today": today})


def createMenu():
    foods = {}
    recipes = Recipe.objects.all()
    if recipes.count() < 7:
        # We need all recipes and blank objects to fill one full week
        dayCount = 0
        rndrecipes = {}
        while dayCount < recipes.count():
            rndrecipes[dayCount] = recipes[dayCount]
            dayCount += 1
        while dayCount < 7:
            rndrecipes[dayCount] = dayCount
            dayCount += 1
        random.shuffle(rndrecipes)
    else:
        rndrecipes = random.sample(recipes, k=7)

    # now build the foods object
    for i in range(7):
        ingredients = []
        if isinstance(rndrecipes[i], Recipe):
            for ing in rndrecipes[i].ingredients.all():
                ingredients.append(ing.name)
            foods[i] = {
                'name': rndrecipes[i].name,
                'book': rndrecipes[i].book,
                'url': rndrecipes[i].url,
                'ingredients': ingredients
            }
        else:
            foods[i] = {
                'name': 'Eat Out',
                'book': '',
                'url': '',
                'ingredients': ingredients
            }

    return foods


@login_required
def menu(request):
    """
    Shows a list of menus
    """

    # Check if database has a menu, if so display it.
    rec = RecipeMenu.objects.filter(owner=request.user)
    if rec.count() > 0:
        # get first one
        foods = json.loads(rec[0].foods)
        date = rec[0].date
        return render(request, 'menu.tmpl', {'foods': foods, "menuactive": True, "menudate": date })

    # Create menu and show it
    foods = createMenu()
    newmenu = RecipeMenu(foods=json.dumps(foods), owner=request.user)
    newmenu.save()
    date = newmenu.date

    return render(request, 'menu.tmpl', {'foods': foods, "menuactive": True, "menudate": date })


@login_required
def editrecipe(request, pk):
    """
    Edit a recipe and its ingredients
    """
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.owner != request.user:
        raise PermissionDenied

    form = CreateRecipe(request.POST or None, instance=recipe)
    formset = IngredientsFormset(request.POST or None, instance=recipe)
    context = {'form': form, 'formset_title': 'Ingredients'}

    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Save successful")
            context['formset'] = IngredientsFormset(instance=recipe)
            return render(request, 'edit.tmpl', context)

    context['formset'] = formset
    return render(request, 'edit.tmpl', context)


@login_required
def editformset(request, pk):
    """
    This is a second form that displays recipe details in tabs.
    """
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.owner != request.user:
        raise PermissionDenied

    form = CreateRecipe(request.POST or None, instance=recipe)
    formset = IngredientsFormset(request.POST or None, instance=recipe)

    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Save successful")
            context = {'form': form, 'formset': IngredientsFormset(instance=recipe)}
            return render(request, 'formset.tmpl', context)

    context = {'form': form, 'formset': formset}
    return render(request, 'formset.tmpl', context)


class RecipeList(LoginRequiredMixin, ListView):
    model = Recipe
    # override the default {app}.{model_viewtype}.tmpl which is foodmenu.recipe_list.tmpl
    template_name = "recipe_list.tmpl"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['homeactive'] = "active"
        return context

    def get_queryset(self):
        return Recipe.objects.filter(owner=self.request.user).order_by('name')


class RecipeCreateView(LoginRequiredMixin, CreateView):
    form_class = CreateRecipe
    template_name = "recipe_create.tmpl"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newactive'] = "active"
        if self.request.POST:
            context["ingredients"] = IngredientsFormset(self.request.POST)
        else:
            context["ingredients"] = IngredientsFormset()
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('listview')

    # Can also use the recipe_create.tmpl then this won't be needed
    def form_valid(self, form):
       form.instance.owner = self.request.user
       return super().form_valid(form)


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    # use permissions to restrict access to delete
    # https://stackoverflow.com/questions/43496708/view-list-of-only-current-user-objects-django-rest
    model = Recipe
    template_name = "confirm_delete.tmpl"

    def get_success_url(self, **kwargs):
        return reverse_lazy('listview')
