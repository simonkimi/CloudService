from time import time
from django.db import models
from user.models import User


class OperateModel(models.Model):
    operate_choice = (
        (0, "正常"),
        (1, "警告"),
        (2, "错误")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.IntegerField(default=time, blank=True)
    desc = models.TextField()
    desc_type = models.IntegerField(choices=operate_choice, default=0)

    class Meta:
        db_table = 'operate'
