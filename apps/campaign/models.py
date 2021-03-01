from django.db import models
from time import time
from explore.models import EarningBaseModel
from user.models import User


class CampaignModel(EarningBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    map = models.CharField(max_length=128, help_text='战役地图')
    create_time = models.IntegerField(default=time, help_text='创建时间')

    class Meta:
        db_table = 'campaign'
