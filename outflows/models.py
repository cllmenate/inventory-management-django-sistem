from django.db import models
from products.models import Product


# Create your models here.
class Outflows(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='outflows'
    )
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Saída'
        verbose_name_plural = 'Saídas'

    def __str__(self):
        return str(self.product)
