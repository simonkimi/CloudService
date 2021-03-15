import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cloudService.settings')
import django
from django.db.models import Q, F

django.setup()

from user.models import UserProfile

UserProfile.objects.all().update(point=F('point') + 4)

