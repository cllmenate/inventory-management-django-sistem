from django.contrib import admin
from products import models


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'product_model',
        'product_model__brand',
        'category',
        'serial_number',
        'quantity',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'title',
        'product_model__name',
        'product_model__brand__name',
        'category__name',
        'serial_number',
    )
    list_filter = (
        'product_model__name',
        'product_model__brand__name',
        'category__name',
    )


admin.site.register(models.Product, ProductAdmin)
