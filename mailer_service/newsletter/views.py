from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView


# Create your views here.

class IndexView(TemplateView):
    """Контроллер просмотра домашней страницы"""
    template_name = 'index.html'
    success_url = reverse_lazy('newsletter:main')


