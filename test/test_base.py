import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cloudService.settings')
import django


django.setup()

from password.models import PasswordModel

print(all([True, True, True]))