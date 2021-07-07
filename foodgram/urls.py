from django.conf import settings
from django.conf.urls import handler400, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

handler400 = 'foodgram.views.bad_request'  # noqa
handler404 = 'foodgram.views.page_not_found'  # noqa
handler500 = 'foodgram.views.server_error'  # noqa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', include('about.urls')),
    path('api/', include('api.urls')),
#    path('cart/', include('cart.urls')),
    path('', include('users.urls')),
    path('', include('recipes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
