from django.db import models


# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

    def __str__(self):
        return self.name
