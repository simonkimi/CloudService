from rest_framework import serializers
from .models import PvpModel


class PvpListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PvpModel
        fields = (
            'username',
            'uid',
            'ships',
            'result'
        )
