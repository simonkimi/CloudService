from rest_framework import serializers
from rest_framework.authtoken.models import Token
from game.net_sender import NetSender
from .models import User, UserProfile


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(help_text='用户名')
    password = serializers.CharField(help_text='密码')

    def validate(self, attrs):
        try:
            user = User.objects.get(username=attrs['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError(f'账号或密码错误!')
        if user.check_password(attrs['password']):
            attrs['user'] = user
            return attrs
        raise serializers.ValidationError('账号或密码错误!')

    def save(self, **kwargs):
        user = self.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return token.key

    class Meta:
        fields = ('username', 'password')


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(help_text='用户名')
    password = serializers.CharField(help_text='密码')
    server = serializers.IntegerField(help_text='服务器')

    def validate(self, attrs):
        try:
            User.objects.get(username=attrs['username'])
            raise serializers.ValidationError(f'用户已存在')
        except User.DoesNotExist:
            pass
        try:
            NetSender().login(
                username=attrs['username'],
                password=attrs['password'],
                server=attrs['server']
            )
        except Exception as e:
            raise serializers.ValidationError(f'验证失败: {str(e)}')
        return attrs

    def save(self, **kwargs):
        user = User.objects.create_user(
            username=self.validated_data['username'],
            password=self.validated_data['password'],
            server=self.validated_data['server']
        )
        token, created = Token.objects.get_or_create(user=user)
        return token.key

    class Meta:
        fields = ('username', 'password', 'server')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'server',
            'switch',
            'point',
            'last_time',
            'next_time',
            'explore_switch',
            'campaign_map',
            'campaign_format',
            'pvp_fleet',
            'pvp_format',
            'pvp_night',
            'pvp_last',
            'repair_switch',
        )


class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'user_profile')
