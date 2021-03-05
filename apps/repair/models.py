from django.db import models
from time import time
from user.models import User


class RepairModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, help_text='泡澡名称')
    create_time = models.IntegerField(default=time)

    class Meta:
        db_table = 'repair'


class RepairMemory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, help_text='泡澡名称')
    start_time = models.IntegerField(help_text='开始时间')
    end_time = models.IntegerField(help_text='结束时间')

    class Meta:
        db_table = 'repair_memory'
