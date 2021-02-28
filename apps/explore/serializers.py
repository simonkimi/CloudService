from rest_framework import serializers
from django.db.models import Sum
from .models import ExploreModel


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
            'dd_cube',
            'cl_cube',
            'bb_cube',
            'cv_cube',
            'ss_cube',
            'fast_repair',
            'fast_build',
            'build_map',
            'equipment_map',
        )


class StatisticSerializer(serializers.Serializer):
    start_time = serializers.IntegerField(help_text='开始时间', read_only=True)
    end_time = serializers.IntegerField(help_text='结束时间', read_only=True)

    def save(self, **kwargs):
        user = self.context['user']
        min_time = min(self.validated_data['end_time'], self.validated_data['start_time'])
        max_time = min(self.validated_data['end_time'], self.validated_data['start_time'])

        queryset = ExploreModel.objects \
            .filter(user=user) \
            .filter(create_time__gte=min_time) \
            .filter(create_time__lt=max_time)

        return {
            'oil': queryset.aggregate(Sum('oil')),
            'ammo': queryset.aggregate(Sum('ammo')),
            'steel': queryset.aggregate(Sum('steel')),
            'aluminium': queryset.aggregate(Sum('aluminium')),
            'dd_cube': queryset.aggregate(Sum('dd_cube')),
            'cl_cube': queryset.aggregate(Sum('cl_cube')),
            'bb_cube': queryset.aggregate(Sum('bb_cube')),
            'cv_cube': queryset.aggregate(Sum('cv_cube')),
            'ss_cube': queryset.aggregate(Sum('ss_cube')),
            'fast_repair': queryset.aggregate(Sum('fast_repair')),
            'fast_build': queryset.aggregate(Sum('fast_build')),
            'build_map': queryset.aggregate(Sum('build_map')),
            'equipment_map': queryset.aggregate(Sum('equipment_map')),
        }
