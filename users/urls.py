from django.urls import include, path

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.SignUp.as_view(), name='register'),
    path('my_subscriptions/', views.subscriptions, name='subscriptions'),
    path('subscriptions/', views.subscriptions_add, name='subscriptions_add'),
    path('subscriptions/<int:user_id>/', views.subscriptions_remove,
         name='subscriptions_remove')
]
