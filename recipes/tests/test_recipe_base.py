from django.test import TestCase
from recipes import views
from recipes.models import Category, Recipe, User



class TestRecipeBase(TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def make_author(self, username='kzmiro'
                        ,email='kzmiro@gmail.com'
                        ,password="123456"
                        , first_name="luiz"
                        , last_name="kzmiro"):
        
        author = User.objects.create_user(username = username
                                         ,email = email
                                         ,password = password
                                         ,first_name = first_name
                                         ,last_name = last_name)
        return author

    def make_category(self, name: str = 'nova categoria'):
        categoria = Category.objects.create(name=name)
        return categoria
    
    def make_recipe(self,
            category_data = None,
            author_data = None,
            title = 'teste',
            description = 'teste',
            slug = 'teste-teste',
            preparation_time = 15,
            preparation_time_unit = 'minutos',
            servings = 5,
            servings_unit = 'porções',
            preparation_step = 'preparação',
            preparation_step_is_html = False,
            is_published = True,):

        if category_data is None:
            category_data = {}
        
        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category = self.make_category(**category_data),
            author = self.make_author(**author_data),
            title = title,
            description = description,
            slug = slug,
            preparation_time = preparation_time,
            preparation_time_unit = preparation_time_unit,
            servings = servings,
            servings_unit = servings_unit,
            preparation_step = preparation_step,
            preparation_step_is_html = preparation_step_is_html,
            is_published = is_published,

        )
        