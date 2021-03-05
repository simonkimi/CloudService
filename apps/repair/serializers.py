from rest_framework import serializers
from .models import RepairModel, RepairMemory


class RepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairModel
        fields = (
            'name',
            'create_time'
        )


class RepairMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairMemory
        fields = [
            'name',
            'start_time',
            'end_time'
        ]
