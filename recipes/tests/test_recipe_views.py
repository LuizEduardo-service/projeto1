from django.urls import reverse, resolve
from recipes import views
from recipes.models import Recipe

from . test_recipe_base import TestRecipeBase

class RecipeViewsTest(TestRecipeBase):
    # HOME ###########################################################
    def test_recipe_home_view_function_is_correct(self):
        view =resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_return_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        
    def test_recipe_home_loads_templates(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'Nenhuma receita cadastrada!',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')

        self.assertIn('Recipes', content)
        self.assertEqual(len(response.context['recipes']), 1)

    def test_recipe_home_template_dont_lod_recipes_not_published(self):
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            'Nenhuma receita cadastrada!', response.content.decode('utf-8')
        )
    # CATEGORY #######################################################
    def test_recipe_category_view_function_is_correct(self):
        view =resolve(
            reverse('recipes:category', kwargs={"category_id": 1})
        )
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_return_404_if_no_recipe_found(self):
        Recipe.objects.filter(pk=1).delete()
        response = self.client.get(reverse('recipes:category', kwargs={"category_id": 10000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        self.make_recipe(title='teste categoria')
        response = self.client.get(reverse('recipes:category', kwargs={"category_id": 1}))
        content = response.content.decode('utf-8')

        self.assertIn('teste categoria', content)
        self.assertEqual(len(response.context['recipes']), 1)

    def test_recipe_category_template_dont_lod_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:category', kwargs={"category_id": recipe.category.id}))

        self.assertEqual(response.status_code, 404)
    
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



