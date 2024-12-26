from django.test import TestCase as DjangoTestCase
from unittest import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse

class AuthorRegisterFormUnitTest(TestCase):

    @parameterized.expand([
        ('username', 'Digite seu nome'),
        ('email', 'Digite seu email'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder_param):
        form = RegisterForm()
        placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder_param, placeholder)

    @parameterized.expand([
        ('email', 'Digite um email válido'),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)       

    @parameterized.expand([
        ('username', 'Nome de usuário'),
        ('first_name', 'Nome'),
        ('last_name', 'Sobrenome'),
        ('email', 'Email'),
        ('password', 'Senha'),
    ])
    def test_fields_labels(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)       

class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': "user",
            'first_name': 'first',
            'last_name': 'last',
            'email': 'luiz@gmail.com',
            'password': 'StrongPassword@1',
            'password2': 'StrongPassword@1',
            }
        
        return super().setUp(*args, **kwargs)
    
    @parameterized.expand([
        ('username', 'Esse campo não deve ser vazio'),
        ('first_name', 'Digite seu primeiro nome'),
        ('last_name', 'Digite seu ultimo nome'),

    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        # self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_send_get_request_to_registration_create_view_return_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):

        url = reverse('authors:create')
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn('Email existente na base de dados!', response.context['form'].errors.get('email'))

    
    def test_author_create_can_login(self):
        url =reverse('authors:create')

        self.form_data.update({
            'username': 'usernameTest',
            'password': '@Pass123',
            'password2': '@Pass123',
        }
        )
        self.client.post(url,data=self.form_data,follow=True)
        is_authenticated = self.client.login(
            username='usernameTest',
            password='@Pass123',
        )

        self.assertTrue(is_authenticated)

