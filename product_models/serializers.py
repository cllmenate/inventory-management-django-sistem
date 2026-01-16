from rest_framework import serializers

from product_models.models import ProductModel


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = "__all__"
