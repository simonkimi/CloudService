from django.db.models import Sum, Count
from rest_framework import serializers
from .models import PvpModel
from time import time


class PvpListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PvpModel
        fields = (
            'username',
            'uid',
            'ships',
            'result',
            'create_time'
        )


class StatisticSerializer(serializers.Serializer):
    start_time = serializers.IntegerField(help_text='开始时间', write_only=True, default=0, allow_null=True)
    end_time = serializers.IntegerField(help_text='结束时间', write_only=True, default=time, allow_null=True)

    def save(self, **kwargs):
        user = self.context['user']
        min_time = min(self.validated_data['end_time'], self.validated_data['start_time'])
        max_time = max(self.validated_data['end_time'], self.validated_data['start_time'])

        queryset = PvpModel.objects \
            .filter(user=user) \
            .filter(create_time__gte=min_time) \
            .filter(create_time__lt=max_time)

        ss = queryset.filter(result=1).count()
        s = queryset.filter(result=2).count()
        a = queryset.filter(result=3).count()
        b = queryset.filter(result=4).count()
        c = queryset.filter(result=5).count()
        d = queryset.filter(result=6).count()
        return {
            'ss': ss,
            's': s,
            'a': a,
            'b': b,
            'c': c,
            'd': d
        }

    class Meta:
        fields = (
            'start_time',
            'end_time'
        )
