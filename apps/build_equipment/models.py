from time import time
from django.db import models
from user.models import User


class BuildEquipmentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cid = models.IntegerField(help_text='装备cid')
    create_time = models.IntegerField(default=time)

    class Meta:
        db_table = 'build_equipment'
