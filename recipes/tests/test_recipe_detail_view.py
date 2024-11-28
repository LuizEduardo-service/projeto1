from django.urls import reverse, resolve
from recipes import views
from recipes.models import Recipe

from . test_recipe_base import TestRecipeBase

class RecipeDetailViewTest(TestRecipeBase):
    
    # DETAIL #######################################################
    def test_recipe_detail_view_function_is_correct(self):
        view =resolve(
            reverse('recipes:recipe', kwargs={"id": 1})
        )
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_return_404_if_no_recipe_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={"id": 10000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_recipes(self):
        title = 'essa é uma pagina de detalhe - e carrega uma unica receita'
        self.make_recipe(title=title)
        response = self.client.get(reverse('recipes:recipe', kwargs={"id": 1}))
        content = response.content.decode('utf-8')

        self.assertIn(title, content)

    def test_recipe_detail_template_dont_lod_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:recipe', kwargs={"id": recipe.pk}))

        self.assertEqual(response.status_code, 404)
