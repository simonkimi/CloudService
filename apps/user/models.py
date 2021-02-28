from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, username, password, server, is_superuser=False):
        user = User.objects.create(username=username)
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save()
        user_profile = UserProfile.objects.create(user=user, server=server)
        user_profile.save()
        return user

    def create_superuser(self, username, password):
        return self.create_user(username=username, password=password, is_superuser=True)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name="学号", max_length=12, null=False, blank=False, unique=True)
    password = models.CharField(verbose_name="密码", max_length=100, null=False, blank=False)
    is_superuser = models.BooleanField(verbose_name="管理员", default=False)

    USERNAME_FIELD = 'username'
    objects = UserManager()


class UserProfile(models.Model):
    user = models.OneToOneField(User, models.CASCADE, related_name='user_profile')
    username = models.CharField(max_length=24, help_text='用户名')

    server = models.IntegerField(help_text='服务器')

    switch = models.BooleanField(default=False, help_text='总开关')

    point = models.IntegerField(default=7, help_text='点数')

    explore_day = models.IntegerField(default=0, help_text='最后扣点时间')
    addition_day = models.IntegerField(default=0, help_text='增值扣点数时间')

    last_time = models.IntegerField(default=0, help_text='上次登录时间')
    next_time = models.IntegerField(default=0, help_text='下次登录时间')

    explore_switch = models.BooleanField(default=False, help_text='远征开关')

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
