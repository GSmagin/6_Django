from django.urls import path

from .apps import MainConfig
from .views import base, contacts, not_found

app_name = MainConfig.name

urlpatterns = [
    path('', base, name='main'),
    path('contacts/', contacts, name='contacts'),
    path('not_found/', not_found, name='not_found'),
]
