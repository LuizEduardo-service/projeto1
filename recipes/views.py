from django.shortcuts import render
from django.http.response import HttpResponse


def home(request):
    return render(request, 'recipes/pages/home.html', context={"name": "Luiz Eduardo"})

def recipe(request, id: int):
    return render(request, 'recipes/pages/recipe-view.html', context={"name": "Luiz Eduardo"})

