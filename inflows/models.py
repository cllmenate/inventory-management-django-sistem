from django.db import models
from suppliers.models import Supplier
from products.models import Product


# Create your models here.
class Inflows(models.Model):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name='inflows'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='inflows'
    )
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'

    def __str__(self):
        return str(self.product)
