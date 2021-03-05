import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cloudService.settings')
import django

django.setup()


# from explore.models import ExploreModel, User
#
# user = User.objects.get(username='simon_xu')
#
# ExploreModel.objects.filter(user=user).delete()

data = {1, 2, 3, 4}

dock = [3, 4]

result = {7, 8, 9}

result.update([i for i in data if i in dock])

print(result)

