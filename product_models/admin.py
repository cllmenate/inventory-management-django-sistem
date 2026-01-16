from django.contrib import admin

from product_models.models import ProductModel


# Register your models here.
class ProductModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "description",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "name",
        "brand__name",
    )
    list_filter = ("brand__name",)


admin.site.register(ProductModel, ProductModelAdmin)
