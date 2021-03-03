import datetime
import time
from asynchronous.app import app
from django.db.models import F, Q

from game.main import ExploreMain
from user.models import UserProfile, User


@app.task()
def execute(username: str):
    try:
        user = User.objects.get(username=username)
        print(f'开始用户{user.username}')
        ExploreMain(user).main()
    except Exception as e:
        print(f"执行任务出错{str(e)}")


@app.task()
def find_need_operate_user():
    print("开始寻找可以操作的对象...")
    hour = datetime.datetime.now().hour
    now_day = (datetime.datetime.now().date() - datetime.date(2014, 2, 1)).days
    now_pvp = "1" if 0 <= hour <= 12 else "2" if 12 <= hour <= 18 else "3"
    now_time = int(time.time())
    pvp_day = f"{now_day}_{now_pvp}"

    user_list = set()

    user_profile = UserProfile.objects.all()
    user_profile.filter(~Q(addition_day=now_day)
                        & (~Q(campaign_map=0) | ~Q(pvp_fleet=0) | ~Q(build_switch=True) | ~Q(equipment_switch=True))
                        & Q(point__gt=0)
                        & Q(switch=True)) \
        .update(point=F("point") - 1, addition_day=now_day)

    user_profile.filter(~Q(explore_day=now_day) & Q(point__gt=0)) \
        .update(point=F("point") - 1, explore_day=now_day)

    user_profile.filter(point__lte=0).update(switch=False)

    # 远征
    user_profile_explore = user_profile.filter(
        Q(next_time__lte=now_time)
        & Q(explore_switch=True)
        & Q(switch=True)
        & Q(point__gt=0)
    )
    for user in user_profile_explore:
        user_list.add(user.user)
        user.save(update_fields=['next_time'])

    # 战役
    user_profile_campaign = user_profile.filter(
        ~Q(campaign_map=0)
        & ~Q(campaign_last=now_day)
        & Q(point__gt=0)
        & Q(switch=True)
    )
    for user in user_profile_campaign:
        user_list.add(user.user)
        user.campaign_last = now_day
        user.save(update_fields=['campaign_last'])

    # 演习
    user_profile_pvp = user_profile.filter(
        ~Q(pvp_fleet=0)
        & ~Q(pvp_last=pvp_day)
        & Q(point__gt=0)
        & Q(switch=True)
    )
    for user in user_profile_pvp:
        user_list.add(user.user)
        user.pvp_last = pvp_day
        user.save(update_fields=['pvp_last'])

    for user in user_list:
        profile = UserProfile.objects.get(user=user)
        profile.last_time = now_time
        profile.next_time = now_time + 60 * 60
        profile.save(update_fields=['next_time', 'last_time'])
        execute.delay(user.username)
