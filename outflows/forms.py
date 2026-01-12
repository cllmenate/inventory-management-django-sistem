from django import forms
from django.core.exceptions import ValidationError
from outflows import models


class OutflowForm(forms.ModelForm):

    class Meta:
        model = models.Outflows
        fields = [
            'product',
            'quantity',
            'description',
        ]
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'product': 'Produto',
            'quantity': 'Quantidade',
            'description': 'Descrição',
        }
        error_messages = {
            'product': {
                'required': 'O produto é obrigatório',
            },
            'quantity': {
                'required': 'A quantidade é obrigatória',
            },
            'description': {
                'required': 'A descrição é obrigatória',
            },
        }

    def clean_quantity(self):
        product = self.cleaned_data.get('product')
        quantity = self.cleaned_data.get('quantity')

        if quantity > product.quantity:
            raise ValidationError(
                'A quantidade de saída não pode ser maior que '
                'a quantidade em estoque. '
                f'Produto: {product.title}. '
                f'Quantidade em estoque: {product.quantity}. '
            )

        return quantity
