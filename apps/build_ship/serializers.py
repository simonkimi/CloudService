from rest_framework import serializers
from .models import BuildShipModel


class BuildShipListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildShipModel
        fields = (
            'cid',
            'name',
            'create_time'
        )
