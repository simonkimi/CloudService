from rest_framework import serializers
from .models import BuildEquipmentModel, BuildEquipmentMemory


class BuildEquipmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildEquipmentModel
        fields = (
            'cid',
            'create_time'
        )


class BuildEquipmentMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildEquipmentMemory
        fields = [
            'cid',
            'start_time',
            'end_time'
        ]
