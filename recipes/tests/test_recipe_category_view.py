from django.urls import reverse, resolve
from recipes import views
from recipes.models import Recipe

from . test_recipe_base import TestRecipeBase

class RecipeCategoryViewTest(TestRecipeBase):

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
