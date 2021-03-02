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
            NetSender(username=attrs['username'],
                      password=attrs['password'],
                      server=attrs['server']).login()
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


class UserSettingSerializer(serializers.Serializer):
    server = serializers.IntegerField(allow_null=True)

    switch = serializers.BooleanField(allow_null=True)

    explore_switch = serializers.BooleanField(allow_null=True)

    campaign_map = serializers.IntegerField(allow_null=True)
    campaign_format = serializers.IntegerField(allow_null=True)

    pvp_fleet = serializers.IntegerField(allow_null=True)
    pvp_format = serializers.IntegerField(allow_null=True)
    pvp_night = serializers.BooleanField(allow_null=True)

    repair_switch = serializers.BooleanField(allow_null=True)

    build_switch = serializers.BooleanField(allow_null=True)
    build_oil = serializers.IntegerField(allow_null=True)
    build_ammo = serializers.IntegerField(allow_null=True)
    build_steel = serializers.IntegerField(allow_null=True)
    build_aluminium = serializers.IntegerField(allow_null=True)

    equipment_switch = serializers.BooleanField(allow_null=True)
    equipment_oil = serializers.IntegerField(allow_null=True)
    equipment_ammo = serializers.IntegerField(allow_null=True)
    equipment_steel = serializers.IntegerField(allow_null=True)
    equipment_aluminium = serializers.IntegerField(allow_null=True)

    dorm_event = serializers.BooleanField(allow_null=True)

    @staticmethod
    def _check_attrs_exist(attrs, *args):
        try:
            if index := [i in attrs for i in args].index(False):
                raise serializers.ValidationError(f'不存在:{args[index]}')
        except ValueError:
            pass

    @staticmethod
    def validate_server(value):
        if value is not None:
            if not 0 <= value <= 5:
                raise serializers.ValidationError('服务器不存在')
        return value

    @staticmethod
    def validate_campaign_map(data):
        if data and data not in [0, 101, 102, 201, 202, 301, 302, 401, 402, 501, 502, 601, 602]:
            raise serializers.ValidationError('战役地图不存在')
        return data

    @staticmethod
    def validate_campaign_format(data):
        if data and not 0 <= data <= 4:
            raise serializers.ValidationError('阵型不存在')
        return data

    @staticmethod
    def validate_pvp_format(data):
        if data and not 0 <= data <= 4:
            raise serializers.ValidationError('阵型不存在')
        return data

    def validate(self, attrs):
        if 'user' not in self.context:
            raise serializers.ValidationError('未提供用户')
        if 'campaign_map' in attrs:
            self._check_attrs_exist(attrs, 'campaign_format')
        if 'pvp_fleet' in attrs:
            self._check_attrs_exist(attrs, 'pvp_format', 'pvp_night')
        if 'build_switch' in attrs:
            self._check_attrs_exist(attrs, 'build_oil', 'build_ammo', 'build_steel', 'build_aluminium')
        if 'equipment_switch' in attrs:
            self._check_attrs_exist(attrs, 'equipment_oil', 'equipment_ammo', 'equipment_steel', 'equipment_aluminium')

    def save(self, **kwargs):
        profile = UserProfile.objects.get(user=self.context['user'])
        attrs = self.validated_data

        check = [
            {'key': 'switch'},
            {'key': 'server'},
            {'key': 'explore_switch'},
            {'key': 'repair_switch'},
            {'key': 'dorm_event'},
        ]
