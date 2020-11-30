from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from django.core.exceptions import PermissionDenied
from foodmenu.models import Recipe, RecipeMenu
from foodmenu.forms import CreateRecipe, IngredientsFormset, CreateMenu
import datetime
import random
import json

# authentication
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    today = datetime.datetime.now().date()
    return render(request, "home.tmpl", {"today": today})


def createMenu(user, rtype=None):
    foods = {}
    if rtype:
        recipes = Recipe.objects.filter(owner=user).filter(recipeType=rtype)
    else:
        recipes = Recipe.objects.filter(owner=user)
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
        rids = [r.id for r in recipes]
        rndrids = random.sample(rids, k=7)
        rndrecipes = Recipe.objects.filter(id__in=rndrids)

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
def menuView(request, pk):
    """
    Shows selected menu
    """

    # # Create menu and show it
    # foods = createMenu()
    # newmenu = RecipeMenu(foods=json.dumps(foods), owner=request.user)
    # newmenu.save()
    # date = newmenu.date

    recipe = get_object_or_404(RecipeMenu, pk=pk)
    if recipe.owner != request.user:
        raise PermissionDenied
    
    foods = json.loads(recipe.foods)
    return render(request, 'menu.tmpl', {'foods': foods, "menuactive": True, "menudate": recipe.date})


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
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['homeactive'] = "active"
        return context

    def get_queryset(self):
        order_by = self.request.GET.get('order', None)
        ftype = self.request.GET.get('ft', None)  # recipeType options
        recs = Recipe.objects.filter(owner=self.request.user)
        if ftype:
            recs = recs.filter(recipeType=ftype)
        if order_by:
            recs = recs.order_by(order_by)
        return recs


class RecipeCreateView(LoginRequiredMixin, CreateView):
    form_class = CreateRecipe
    template_name = "recipe_create.tmpl"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != self.request.user:
            raise PermissionDenied
        # we use get instead of post to get a confirmation
        return super().get(request, *args, **kwargs)


class RecipeMenuList(LoginRequiredMixin, ListView):
    model = RecipeMenu
    # override the default {app}.{model_viewtype}.tmpl which is foodmenu.recipe_list.tmpl
    template_name = "recipemenu_list.tmpl"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menuactive'] = "active"
        return context

    def get_queryset(self):
        return RecipeMenu.objects.filter(owner=self.request.user)


class MenuCreateView(LoginRequiredMixin, CreateView):
    form_class = CreateMenu
    template_name = "menu_new.tmpl"

    def get_success_url(self, **kwargs):
        return reverse_lazy('menulist')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        # FIXME allow user to select meal types
        form.instance.foods = json.dumps(createMenu(self.request.user, "Dinner"))
        return super().form_valid(form)


class RecipeMenuDelete(LoginRequiredMixin, DeleteView):
    model = RecipeMenu
    template_name = "confirm_delete.tmpl"

    def get_success_url(self, **kwargs):
        return reverse_lazy('menulist')
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != self.request.user:
            raise PermissionDenied
        # we use get instead of post to get a confirmation
        return super().get(request, *args, **kwargs)