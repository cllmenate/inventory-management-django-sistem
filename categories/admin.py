from django.contrib import admin
from categories import models


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at',)
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at',)


admin.site.register(models.Category, CategoryAdmin)
