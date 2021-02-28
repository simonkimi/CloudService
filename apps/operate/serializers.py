from rest_framework import serializers
from .models import OperateModel


class OperateListSerializers(serializers.ModelSerializer):
    class Meta:
        model = OperateModel
        fields = (
            'create_time',
            'desc',
            'type'
        )
