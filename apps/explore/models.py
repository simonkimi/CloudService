from django.db import models
from user.models import User, EarningBaseModel
from time import time


class ExploreModel(EarningBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    map = models.CharField(max_length=128, help_text='远征地图')
    success = models.BooleanField(help_text='大成功', default=False)
    create_time = models.IntegerField(default=time, help_text='创建时间')

    class Meta:
        db_table = 'explore'


class ExploreMemory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    map = models.CharField(max_length=128, help_text='远征地图')
    start_time = models.IntegerField(help_text='开始时间')
    end_time = models.IntegerField(help_text='结束时间')

    class Meta:
        db_table = 'explore_memory'
