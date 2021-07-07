from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes import views

js_router = DefaultRouter()
js_router.register('purchases', views.CartViewSet, basename='purchases')

urlpatterns = [
    path('', views.index, name='index'),
    path('', include(js_router.urls)),    path('favorites/', views.favorites, name='favorites'),
    path('new_recipe/', views.create_recipe, name='create_recipe'),
    path('recipes/<slug:slug>/', views.recipe_detail,
         name='recipe_detail'),
    path('recipes/<int:user_id>/<slug:slug>/edit/', views.edit_recipe,
         name='edit_recipe'),
    path('recipes/<int:user_id>/<slug:slug>/delete/', views.recipe_delete,
         name='recipe_delete'),
    path('cart/', views.cart, name='cart'),
    path('cart_download/', views.cart_download, name='cart_download'),
    path('users/<str:username>/', views.profile, name='profile'),
]
