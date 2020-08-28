from django.urls import path
from foodmenu.views import RecipeList, RecipeCreateView, RecipeDeleteView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu', views.menu, name="menu"),
    # path('generatemenu', views.generate_menu, name="generatemenu"),
    path('recipes', RecipeList.as_view(), name='listview'),
    path('newrecipe', RecipeCreateView.as_view(), name="createrecipe"),
    path('<int:pk>/delete', RecipeDeleteView.as_view(), name='deleterecipe'),
    path('<int:pk>/edit', views.editrecipe, name='editrecipe')
]
