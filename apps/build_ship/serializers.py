from rest_framework import serializers
from .models import BuildShipModel, BuildShipMemory


class BuildShipListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildShipModel
        fields = (
            'cid',
            'name',
            'create_time'
        )


class BuildShipMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildShipMemory
        fields = [
            'type',
            'start_time',
            'end_time'
        ]
