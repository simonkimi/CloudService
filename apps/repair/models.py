from django.db import models
from time import time
from user.models import User


class RepairModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, help_text='泡澡名称')
    create_time = models.IntegerField(default=time)

    class Meta:
        db_table = 'repair'
