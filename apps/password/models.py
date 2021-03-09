from django.db import models
from user.models import User


class PasswordModel(models.Model):
    code = models.CharField(max_length=10, help_text='激活码', primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    activity_time = models.IntegerField(default=0, help_text='使用时间')
    point = models.IntegerField(default=30, help_text='包含点数')

    class Meta:
        db_table = 'password'
