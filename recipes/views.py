from django.http.response import Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from recipes.models import Recipe
from django.db.models import Q

def home(request):

    recipes = Recipe.objects.filter(is_published= True).all().order_by('-id')
    return render(request, 'recipes/pages/home.html', context={"recipes": recipes})

def category(request, category_id: int):
    recipe_category = get_list_or_404(Recipe.objects.filter(
        category__id=category_id,
        is_published = True,)
        .order_by('-id'))

    return render(request, 'recipes/pages/category.html',
                  context={"recipes": recipe_category,
                           'title': f'{recipe_category[0].category.name}  - Category '})

def recipe(request, id: int):
    recipe = get_object_or_404(Recipe,
        pk=id,
        is_published = True, )
    return render(request, 'recipes/pages/recipe-view.html',
                  context={"recipe": recipe, 'is_detail_page': True}
                  )

def search(request):

    search_text = str(request.GET.get('search')).strip()

    if not search_text:
        raise Http404()
    
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains = search_text) |
            Q(description__icontains = search_text)
        ),
        is_published = True
    )
    return render(request, 'recipes/pages/search.html',{
        'page_title': f'pesquisa por "{search_text}"',
        'search_text': search_text,
        'recipes': recipes
    })