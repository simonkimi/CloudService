import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cloudService.settings')
import django
from django.db.models import Q

django.setup()

from user.models import UserProfile

user_profile = UserProfile.objects.all().filter(
    (~Q(campaign_map=0) | ~Q(pvp_fleet=0) | Q(build_switch=True) | Q(equipment_switch=True))
    & Q(point__gt=0)
    & Q(switch=True))

for i in user_profile:
    print(i.campaign_map != 0 or i.pvp_fleet != 0 or i.build_switch or i.equipment_switch)
