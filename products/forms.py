from django import forms

from products import models


class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = [
            "title",
            "product_model",
            "category",
            "description",
            "serial_number",
            "cost_price",
            "sell_price",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "product_model": forms.Select(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "serial_number": forms.TextInput(attrs={"class": "form-control"}),
            "cost_price": forms.NumberInput(attrs={"class": "form-control"}),
            "sell_price": forms.NumberInput(attrs={"class": "form-control"}),
        }
        labels = {
            "title": "Título",
            "product_model": "Modelo",
            "category": "Categoria",
            "description": "Descrição",
            "serial_number": "Número de Série",
            "cost_price": "Preço de Custo",
            "sell_price": "Preço de Venda",
        }
        error_messages = {
            "title": {
                "required": "O título é obrigatório",
            },
            "product_model": {
                "required": "O modelo é obrigatório",
            },
            "category": {
                "required": "A categoria é obrigatória",
            },
            "description": {
                "required": "A descrição é obrigatória",
            },
            "serial_number": {
                "required": "O número de série é obrigatório",
            },
            "cost_price": {
                "required": "O preço de custo é obrigatório",
            },
            "sell_price": {
                "required": "O preço de venda é obrigatório",
            },
        }
