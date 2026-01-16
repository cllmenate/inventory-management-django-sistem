from django.db import models

from brands.models import Brand


class ProductModel(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Modelo de Produto"
        verbose_name_plural = "Modelos de Produto"

    def __str__(self):
        return f"{self.name} - {self.brand}"
