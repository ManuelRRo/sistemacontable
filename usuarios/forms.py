from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User
from django import forms

class RegisterUserForm(UserCreationForm):
	password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user','placeholder':'Contraseña'}),
    )
	password2 = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user','placeholder':'Confirmar Contraseña'}),
	)
	class Meta:
		model = User
		fields = ('username','email','password1','password2')
		widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-user','placeholder':'Nombre de Usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-user','placeholder':'Correo'}),
        }