from django import forms
from .models import Catalogo

class CatalagoForm(forms.ModelForm):

    class Meta:
        model = Catalogo
        fields = ['nombre_catalogo','archivo']
