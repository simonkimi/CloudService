from rest_framework import serializers
from django.db.models import Sum
from .models import ExploreModel, ExploreMemory
from time import time


class ExploreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExploreModel
        fields = (
            'map',
            'create_time',
            'oil',
            'ammo',
            'steel',
            'aluminium',
            'fast_repair',
            'fast_build',
            'build_map',
            'equipment_map',
        )


class StatisticSerializer(serializers.Serializer):
    start_time = serializers.IntegerField(help_text='开始时间', write_only=True, default=0, allow_null=True)
    end_time = serializers.IntegerField(help_text='结束时间', write_only=True, default=time, allow_null=True)

    def save(self, **kwargs):
        user = self.context['user']
        min_time = min(self.validated_data['end_time'], self.validated_data['start_time'])
        max_time = max(self.validated_data['end_time'], self.validated_data['start_time'])

        queryset = ExploreModel.objects \
            .filter(user=user) \
            .filter(create_time__gte=min_time) \
            .filter(create_time__lt=max_time)

        sums = queryset.aggregate(
            Sum('oil'), Sum('ammo'), Sum('steel'), Sum('aluminium'),
            Sum('dd_cube'), Sum('cl_cube'), Sum('bb_cube'), Sum('cv_cube'), Sum('ss_cube'),
            Sum('fast_repair'), Sum('fast_build'), Sum('build_map'), Sum('equipment_map'),
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
            'fast_repair': sums['fast_repair__sum'] or 0,
            'fast_build': sums['fast_build__sum'] or 0,
            'build_map': sums['build_map__sum'] or 0,
            'equipment_map': sums['equipment_map__sum'] or 0,
        }

    class Meta:
        fields = (
            'start_time',
            'end_time'
        )


class ExploreMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExploreMemory
        fields = [
            'map',
            'start_time',
            'end_time'
        ]
