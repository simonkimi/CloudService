from time import time
from django.db import models
from user.models import User


class BuildEquipmentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cid = models.IntegerField(default=0, help_text='装备cid')
    create_time = models.IntegerField(default=time)

    class Meta:
        db_table = 'build_equipment'


class BuildEquipmentMemory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.IntegerField(help_text='开始时间')
    end_time = models.IntegerField(help_text='结束时间')
    cid = models.IntegerField(help_text='装备cid')

    class Meta:
        db_table = 'build_equipment_memory'
