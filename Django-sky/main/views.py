from django.shortcuts import render


def base(request):
    return render(request, 'main/index.html')


def contacts(request):
    return render(request, 'main/contacts.html')

