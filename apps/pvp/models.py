from django.db import models
from user.models import User


class PvpModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=128, help_text='对方名称')
    uid = models.IntegerField(help_text='对方uid')
    ships = models.TextField(help_text='舰队船只')
    result = models.IntegerField(help_text='结果')

    class Meta:
        db_table = 'pvp'
