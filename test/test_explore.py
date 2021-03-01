import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cloudService.settings')
import django
import hashlib
import json

django.setup()

from user.models import User
from game.main import ExploreMain

user = User.objects.all()[0]

explore = ExploreMain(user)
explore.main()
