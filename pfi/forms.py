from django import forms
from pfi.models import *


class Usuarioforms(forms.ModelForm):
    class meta:
        model = Usuario
        fields = '__all__'