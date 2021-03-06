from time import time
from django.db.models import Sum
from rest_framework import serializers
from .models import CampaignModel


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignModel
        fields = ('map', 'oil', 'ammo', 'steel', 'aluminium',
                  'dd_cube', 'cl_cube', 'bb_cube', 'cv_cube', 'ss_cube')


class StatisticSerializer(serializers.Serializer):
    start_time = serializers.IntegerField(help_text='开始时间', default=0, write_only=True, allow_null=True)
    end_time = serializers.IntegerField(help_text='结束时间', write_only=True, default=time, allow_null=True)

    def validate(self, attrs):
        attrs['max'] = max(attrs['end_time'], attrs['start_time'])
        attrs['min'] = min(attrs['end_time'], attrs['start_time'])
        return attrs

    def save(self, **kwargs):
        user = self.context['user']

        queryset = CampaignModel.objects \
            .filter(user=user) \
            .filter(create_time__gte=self.validated_data['min']) \
            .filter(create_time__lt=self.validated_data['max'])

        sums = queryset.aggregate(
            Sum('oil'), Sum('ammo'), Sum('steel'), Sum('aluminium'),
            Sum('dd_cube'), Sum('cl_cube'), Sum('bb_cube'), Sum('cv_cube'), Sum('ss_cube'),
        )

        return {
            'oil': sums['oil__sum'] or 0,
            'ammo': sums['ammo__sum'] or 0,
            'steel': sums['steel__sum'] or 0,
            'aluminium': sums['aluminium__sum'] or 0,
            'dd_cube': sums['dd_cube__sum'] or 0,
            'cl_cube': sums['cl_cube__sum'] or 0,
            'bb_cube': sums['bb_cube__sum'] or 0,
            'cv_cube': sums['cv_cube__sum'] or 0,
            'ss_cube': sums['ss_cube__sum'] or 0,
        }

    class Meta:
        fields = (
            'start_time',
            'end_time'
        )
