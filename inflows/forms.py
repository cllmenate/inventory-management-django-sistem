from django import forms

from inflows import models


class InflowForm(forms.ModelForm):
    class Meta:
        model = models.Inflows
        fields = [
            "product",
            "supplier",
            "quantity",
            "description",
        ]
        widgets = {
            "product": forms.Select(attrs={"class": "form-control"}),
            "supplier": forms.Select(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }
        labels = {
            "product": "Produto",
            "supplier": "Fornecedor",
            "quantity": "Quantidade",
            "description": "Descrição",
        }
        error_messages = {
            "product": {
                "required": "O produto é obrigatório",
            },
            "supplier": {
                "required": "O fornecedor é obrigatório",
            },
            "quantity": {
                "required": "A quantidade é obrigatória",
            },
            "description": {
                "required": "A descrição é obrigatória",
            },
        }
