from django.contrib import admin

from inflows import models


# Register your models here.
class InflowAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "supplier",
        "quantity",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "product__title",
        "supplier__name",
    )
    list_filter = (
        "created_at",
        "updated_at",
    )


admin.site.register(models.Inflows, InflowAdmin)
