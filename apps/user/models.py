from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    username = models.CharField(max_length=24, help_text='用户名')

    server = models.IntegerField(help_text='服务器')

    switch = models.BooleanField(default=False, help_text='总开关')

    point = models.IntegerField(default=7, help_text='点数')

    explore_day = models.IntegerField(default=0, help_text='最后扣点时间')
    addition_day = models.IntegerField(default=0, help_text='增值扣点数时间')

    last_time = models.IntegerField(default=0, help_text='上次登录时间')
    next_time = models.IntegerField(default=0, help_text='下次登录时间')

    explore_switch = models.BooleanField(default=False, help_text='远征开关')
    explore_memory = models.CharField(default="{}", max_length=128, help_text='远征记忆')

    campaign_map = models.IntegerField(default=0, help_text='战役地图')
    campaign_format = models.IntegerField(default=1, help_text='战役队形')
    campaign_last = models.IntegerField(default=0, help_text='上次战役时间')

    pvp_fleet = models.IntegerField(default=0, help_text='战役队伍')
    pvp_format = models.IntegerField(default=1, help_text='战役阵型')
    pvp_night = models.BooleanField(default=False, help_text='战役夜战')
    pvp_last = models.CharField(default="0_0", max_length=10, help_text='上次战役时间')

    repair_switch = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_profile'
