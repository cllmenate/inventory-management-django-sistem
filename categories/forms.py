from django import forms

from categories import models


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
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
