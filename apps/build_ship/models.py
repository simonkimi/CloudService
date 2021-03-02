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
