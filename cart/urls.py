from django.urls import path

from .views import CartListView, cart_download, cart_remove

urlpatterns = [
    path('', CartListView.as_view(), name='cart_detail'),
    path('remove/<int:id>/', cart_remove, name='cart_remove'),
    path('download/', cart_download, name='cart_download'),
]