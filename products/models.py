from django.db import models
from product_models.models import ProductModel
from categories.models import Category


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=500)
    product_model = models.ForeignKey(
        ProductModel,
        on_delete=models.PROTECT,
        related_name='products'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )
    description = models.TextField(max_length=1000)
    serial_number = models.CharField(max_length=100)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.title
