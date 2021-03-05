from time import time
from django.db import models
from user.models import User


class BuildShipModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, help_text='船只名称')
    cid = models.IntegerField(help_text='船只cid')
    is_new = models.BooleanField(help_text='是否为新船')
    create_time = models.IntegerField(default=time)

    class Meta:
        db_table = 'build_ship'


class BuildShipMemory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.IntegerField(help_text='开始时间')
    end_time = models.IntegerField(help_text='结束时间')
    type = models.IntegerField(help_text='船只类型')

    class Meta:
        db_table = 'build_ship_memory'

