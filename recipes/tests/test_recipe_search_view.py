from django.urls import reverse, resolve
from recipes import views
from recipes.models import Recipe

from .test_recipe_base import TestRecipeBase

class RecipeSearchViewTest(TestRecipeBase):


    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?search=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')


    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_terme_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?search=Teste'
        response = self.client.get(url)
        self.assertIn(
        'pesquisa por &quot;Teste&quot;| Recipes',
        response.content.decode('utf-8')
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = "Receita 1"
        title2 = "Receita 2"

        recipe1 = self.make_recipe(
            slug='receita-1',title=title1,author_data={'username': "luiz"}
        )
        recipe2 = self.make_recipe(
            slug='receita-2',title=title2,author_data={'username': "eduardo"}
        )

        url = reverse('recipes:search')
        response1 = self.client.get(f'{url}?search={title1}')
        response2 = self.client.get(f'{url}?search={title2}')
        response_both = self.client.get(f'{url}?search=Receita')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])