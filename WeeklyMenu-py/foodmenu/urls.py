from django.urls import path
from foodmenu.views import RecipeList, RecipeCreateView, RecipeDeleteView, RecipeMenuList

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menus', RecipeMenuList.as_view(), name="menulist"),
    # path('menus/view/<int:pk>', RecipeMenuItem.as_view(), name="viewmenu"),
    # path('menus/delete/<int:pk>', RecipeMenuDelete.as_view(), name="deletemenu"),
    path('recipes', RecipeList.as_view(), name='listview'),
    path('recipes/new', RecipeCreateView.as_view(), name="createrecipe"),
    path('recipes/delete/<int:pk>', RecipeDeleteView.as_view(), name='deleterecipe'),
    path('recipes/edit/<int:pk>', views.editrecipe, name='editrecipe'),
    # old deprecated url patterns
    path('menu', views.menu, name="menu"),
    path('<int:pk>/delete', RecipeDeleteView.as_view()),
    path('<int:pk>/edit', views.editrecipe)
]
