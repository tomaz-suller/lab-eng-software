from django import forms
from django.forms import TextInput

from .models import CompanhiaAerea


class CompanhiaAereaForm(forms.ModelForm):
    class Meta:
        model = CompanhiaAerea
        fields = [
            "nome",
            "sigla",
        ]

        widgets = {
            "nome": TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 300px;",
                    "placeholder": "Nome",
                }
            ),
            "sigla": TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 300px;",
                    "placeholder": "Sigla",
                }
            ),
        }
