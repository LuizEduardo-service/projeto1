from django.urls import reverse, resolve
from recipes import views
from unittest.mock import patch
from . test_recipe_base import TestRecipeBase

class RecipeHomeViewTest(TestRecipeBase):
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

    def test_recipe_home_is_paginated(self):
        for i in range(18):
            kwargs = {'slug': f'sl{i}', 'author_data': {'username': f'user-{i}'}}
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new= 6):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            pagination = recipes.paginator

            self.assertEqual(pagination.num_pages, 3)
            self.assertEqual(len(pagination.get_page(1)), 6)

