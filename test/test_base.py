import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cloudService.settings')
import django

django.setup()

from user.models import User

user = User.objects.get(username='simon_xu')
user_2 = User.objects.all()[0]

print(user == user_2)
