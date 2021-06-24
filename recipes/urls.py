from django.urls import path

from recipes import views

urlpatterns = [
    path('', views.index, name='index'),
    path('favorites/', views.favorites, name='favorites'),
    path('new_recipe/', views.create_recipe, name='create_recipe'),
    path('recipes/<slug:slug>/', views.recipe_detail,
         name='recipe_detail'),
    path('recipes/<int:user_id>/<slug:slug>/edit/', views.edit_recipe,
         name='edit_recipe'),
    path('recipes/<int:user_id>/<slug:slug>/delete/', views.recipe_delete,
         name='recipe_delete'),
    path('<str:username>/', views.profile, name='profile'),
]
