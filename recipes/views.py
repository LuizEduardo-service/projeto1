from django.shortcuts import render
from django.http.response import HttpResponse


def home(request):
    return render(request, 'recipes/home.html')

def contato(request):
    return HttpResponse('Tela contato')

def sobre(request):
    return HttpResponse('Tela sobre')
