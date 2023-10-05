from django import forms
from .models import Catalogo

class CatalagoForm(forms.ModelForm):

    class Meta:
        model = Catalogo
        fields = ['archivo']

class EmpresaForm(forms.Form):
    nombre_empresa = forms.CharField(max_length=100)
