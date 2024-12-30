from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.func_aux import *
    
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

    first_name = forms.CharField(
        error_messages={'required': 'Digite seu primeiro nome'},
        required= True,
        label= 'Nome'
    )    
    last_name = forms.CharField(
        error_messages={'required': 'Digite seu ultimo nome'},
        required= True,
        label= 'Sobrenome'
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
        
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        email_exists = User.objects.filter(email= email).exists()

        if email_exists:
            raise ValidationError(
                'Email existente na base de dados!', code='invalid'
            )
        return email