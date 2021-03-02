from rest_framework import serializers
from .models import BuildEquipmentModel


class BuildEquipmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildEquipmentModel
        fields = (
            'cid',
            'create_time'
        )
