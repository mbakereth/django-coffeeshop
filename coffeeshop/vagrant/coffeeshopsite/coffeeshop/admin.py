from django.contrib import admin
from django.apps import apps

app = apps.get_app_config('coffeeshop')

for model_name, model in app.models.items():
    if (model_name != "User" and model_name != "Group"):
        admin.site.register(model)
