from django import forms
from .models import UserWeb

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = UserWeb
        fields = ['nome', 'telefone']
