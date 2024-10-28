from django.shortcuts import render
from django.http.response import HttpResponse
from utils.recipes.factory import make_recipe
from recipes.models import Recipe

def home(request):
    # mock_recipes = [make_recipe() for _ in range(10)]
    recipes = Recipe.objects.filter(is_published= True).all().order_by('-id')
    return render(request, 'recipes/pages/home.html', context={"recipes": recipes})

def category(request, category_id: int):
    recipe_category = Recipe.objects.filter(category__id=category_id, is_published = True)
    return render(request, 'recipes/pages/category.html',
                  context={"recipes": recipe_category,
                           'title': f'{recipe_category.first().category.name}  - Category '})

def recipe(request, id: int):
    # mock_recipe = make_recipe()
    recipe = Recipe.objects.filter(id=id).first()
    return render(request, 'recipes/pages/recipe-view.html',
                  context={"recipe": recipe, 'is_detail_page': True}
                  )

