from .models import PasswordModel
from rest_framework import serializers
from time import time
from user.models import UserProfile
from user.serializers import UserProfileSerializer


class ActiveSerializers(serializers.Serializer):
    code = serializers.CharField()

    @staticmethod
    def validate_code(data):
        try:
            password: PasswordModel = PasswordModel.objects.get(code=data)
            if password.user is not None:
                raise serializers.ValidationError('激活码已被使用')
            return data
        except PasswordModel.DoesNotExist:
            raise serializers.ValidationError('激活码不存在')

    def save(self, **kwargs):
        user = self.context['user']
        print(self.validated_data)
        password: PasswordModel = PasswordModel.objects.get(code=self.validated_data['code'])
        password.user = user
        password.activity_time = int(time())
        password.save(update_fields=['user', 'activity_time'])

        user_profile: UserProfile = UserProfile.objects.get(user=user)
        user_profile.point += password.point
        user_profile.save(update_fields=['point'])

        return UserProfileSerializer(user_profile).data
