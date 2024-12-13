from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
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
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'insira seu nome de usuario'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'insira sua senha aqui'
            })
        }
