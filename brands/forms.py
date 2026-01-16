from django import forms

from brands import models


class BrandForm(forms.ModelForm):
    class Meta:
        model = models.Brand
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
        labels = {
            "name": "Nome",
            "description": "Descrição",
        }
        error_messages = {
            "name": {
                "required": "O nome é obrigatório",
            },
        }
