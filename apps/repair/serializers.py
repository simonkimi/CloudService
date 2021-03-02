from rest_framework import serializers
from .models import RepairModel


class RepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairModel
        fields = (
            'name',
            'create_time'
        )
