from rest_framework import serializers
from outflows.models import Outflows


class OutflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outflows
        fields = '__all__'
