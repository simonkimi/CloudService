import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cloudService.settings')
import django


django.setup()

from user.models import UserProfile

UserProfile.objects.all().update(next_time=0, token='')

# from asynchronous.login_task import get_token
# from celery.result import AsyncResult
#
#
# result = get_token.s("simon_xu", 'xusong404', 0)



# print(result())