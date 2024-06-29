from django.urls import path

from .apps import MainConfig
from .views import base, contacts

app_name = MainConfig.name

urlpatterns = [
    path('', base, name='main'),
    path('contacts/', contacts, name='contacts'),
]
