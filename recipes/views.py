from django.shortcuts import render
from django.http.response import HttpResponse
from utils.recipes.factory import make_recipe


def home(request):
    mock_recipes = [make_recipe() for _ in range(10)]
    return render(request, 'recipes/pages/home.html', context={"recipes": mock_recipes})

def recipe(request, id: int):
    mock_recipe = make_recipe()
    return render(request, 'recipes/pages/recipe-view.html',
                  context={"recipe": mock_recipe, 'is_detail_page': True}
                  )

