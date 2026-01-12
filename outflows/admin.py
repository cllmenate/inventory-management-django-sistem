from django.contrib import admin
from outflows import models


# Register your models here.
class OutflowAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'quantity',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'product__title',
    )
    list_filter = ('created_at', 'updated_at',)


admin.site.register(models.Outflows, OutflowAdmin)
