from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()

def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    if not regex.match(password):
        raise ValidationError('Pass deve conter letras maiusculas, minusculas e numeros',code='invalid')
    
class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Digite seu nome')
        add_placeholder(self.fields['email'], 'Digite seu email')
        add_placeholder(self.fields['password'], 'insira sua senha aqui')

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Digite a senha novamente'
            }
        ),
        validators=[strong_password]
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username','email', 'password']
        labels = {
            'username': 'Nome de usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'Email',
            'password': 'Senha',
        }  
        help_texts={
            'email': 'Digite um email válido'
        }   

        error_messages = {
            'username':{
                'required': 'Esse campo não deve ser vazio',
            }
        }  


    def clean(self):
        cleaned_data =  super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': 'Senhas não conferem'
            })