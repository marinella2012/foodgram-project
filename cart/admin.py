from django.apps import apps as django_apps
from django.contrib import admin

app_models = django_apps.get_app_config('recipes').get_models()

for model in app_models:

    try:

        admin.site.register(model)

    except admin.sites.AlreadyRegistered:

        pass
