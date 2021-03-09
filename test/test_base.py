import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cloudService.settings')
import django


django.setup()

from password.models import PasswordModel

PasswordModel.objects.create(
    point=1000,
    code="1234567890"
)
