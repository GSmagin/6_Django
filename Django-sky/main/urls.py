from django.urls import path

from shop.views import contacts
from .apps import MainConfig
from .views import base, not_found

app_name = MainConfig.name

urlpatterns = [
    path('', base, name='main'),
    path('contacts/', contacts, name='contacts'),
    path('not_found/', not_found, name='not_found'),
]
