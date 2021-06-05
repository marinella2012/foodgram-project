from django.urls import include, path

from . import views

urlpatterns = [path('', views.index, name='index'), ]
#    path('subscriptions/', views.subscriptions, name='subscriptions'),
#    path('favorites/', views.favorites, name='favorites')
