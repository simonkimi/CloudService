from django.db import models
from user.models import User
from time import time


class EarningBaseModel(models.Model):
    oil = models.IntegerField(default=0, help_text='油收益')
    ammo = models.IntegerField(default=0, help_text='弹药')
    steel = models.IntegerField(default=0, help_text='钢铁')
    aluminium = models.IntegerField(default=0, help_text='铝')

    dd_cube = models.IntegerField(default=0, help_text='驱逐核心')
    cl_cube = models.IntegerField(default=0, help_text='巡洋核心')
    bb_cube = models.IntegerField(default=0, help_text='战列核心')
    cv_cube = models.IntegerField(default=0, help_text='航母核心')
    ss_cube = models.IntegerField(default=0, help_text='潜艇')

    fast_repair = models.IntegerField(default=0, help_text='快修')
    fast_build = models.IntegerField(default=0, help_text='快建')
    build_map = models.IntegerField(default=0, help_text='建造蓝图')
    equipment_map = models.IntegerField(default=0, help_text='开发蓝图')

    class Meta:
        abstract = True


class ExploreModel(EarningBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    map = models.CharField(max_length=128, help_text='远征地图')
    success = models.BooleanField(help_text='大成功', default=False)
    create_time = models.IntegerField(default=time, help_text='创建时间')

    class Meta:
        db_table = 'explore'
