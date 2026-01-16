from django import forms

from product_models import models


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = models.ProductModel
        fields = [
            "name",
            "brand",
            "description",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "brand": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }
        labels = {
            "name": "Nome",
            "brand": "Marca",
            "description": "Descrição",
        }
        error_messages = {
            "name": {
                "required": "O nome é obrigatório",
            },
            "brand": {
                "required": "A marca é obrigatória",
            },
            "description": {
                "required": "A descrição é obrigatória",
            },
        }
