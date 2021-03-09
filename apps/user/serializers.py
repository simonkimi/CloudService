from rest_framework import serializers
from rest_framework.authtoken.models import Token

from game.main import ExploreMain
from game.net_sender import NetSender
from .models import User, UserProfile, UserResource


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
            sender = NetSender(username=attrs['username'],
                               password=attrs['password'],
                               server=attrs['server']).login()
            attrs['sender'] = sender
        except Exception as e:
            raise serializers.ValidationError(f'用户名或者密码错误: {str(e)}')
        return attrs

    def save(self, **kwargs):
        attrs = self.validated_data
        try:
            user = User.objects.get(username=attrs['username'])
            user.set_password(attrs['password'])
            user.save(update_fields=['password'])
            user_profile = UserProfile.objects.get(user=user)
            user_profile.server = attrs['server']
            user_profile.save(update_fields=['server'])
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=attrs['username'],
                password=attrs['password'],
                server=attrs['server']
            )
        ExploreMain(user=user, sender=attrs['sender']).init_user()
        token, created = Token.objects.get_or_create(user=user)
        return token.key

    class Meta:
        fields = ('username', 'password', 'server')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'username',
            'server',
            'level',
            'sign',
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
            'repair_switch',
            'build_switch',
            'build_oil',
            'build_ammo',
            'build_steel',
            'build_aluminium',
            'equipment_switch',
            'equipment_oil',
            'equipment_ammo',
            'equipment_steel',
            'equipment_aluminium',
            'dorm_event'
        )


class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'user_profile')


class UserSettingSerializer(serializers.Serializer):
    server = serializers.IntegerField(allow_null=True, required=False)

    switch = serializers.BooleanField(allow_null=True, required=False)

    explore_switch = serializers.BooleanField(allow_null=True, required=False)

    campaign_map = serializers.IntegerField(allow_null=True, required=False)
    campaign_format = serializers.IntegerField(allow_null=True, required=False)

    pvp_fleet = serializers.IntegerField(allow_null=True, required=False)
    pvp_format = serializers.IntegerField(allow_null=True, required=False)
    pvp_night = serializers.BooleanField(allow_null=True, required=False)

    repair_switch = serializers.BooleanField(allow_null=True, required=False)

    build_switch = serializers.BooleanField(allow_null=True, required=False)
    build_oil = serializers.IntegerField(allow_null=True, required=False)
    build_ammo = serializers.IntegerField(allow_null=True, required=False)
    build_steel = serializers.IntegerField(allow_null=True, required=False)
    build_aluminium = serializers.IntegerField(allow_null=True, required=False)

    equipment_switch = serializers.BooleanField(allow_null=True, required=False)
    equipment_oil = serializers.IntegerField(allow_null=True, required=False)
    equipment_ammo = serializers.IntegerField(allow_null=True, required=False)
    equipment_steel = serializers.IntegerField(allow_null=True, required=False)
    equipment_aluminium = serializers.IntegerField(allow_null=True, required=False)

    dorm_event = serializers.BooleanField(allow_null=True, required=False)

    dependence = {
        'server': [],
        'switch': [],
        'explore_switch': [],
        'campaign_map': ['campaign_format'],
        'pvp_fleet': ['pvp_format', 'pvp_night'],
        'repair_switch': [],
        'build_switch': ['build_oil', 'build_ammo', 'build_steel', 'build_aluminium'],
        'equipment_switch': ['equipment_oil', 'equipment_ammo', 'equipment_steel', 'equipment_aluminium'],
        'dorm_event': [],
    }

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
        if data and not 1 <= data <= 5:
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
        for key, dependencies in self.dependence.items():
            if key in attrs and attrs[key] is not None:
                try:
                    index = [i in attrs for i in dependencies].index(False)
                    raise serializers.ValidationError(f'{dependencies[index]}未提供')
                except ValueError:
                    pass
        return attrs

    def save(self, **kwargs):
        profile = UserProfile.objects.get(user=self.context['user'])
        attrs = self.validated_data
        update_fields = []
        for key, dependencies in self.dependence.items():
            if key in attrs and attrs[key] is not None:
                profile.__setattr__(key, attrs[key])
                update_fields.append(key)
                for sub_key in dependencies:
                    update_fields.append(sub_key)
                    profile.__setattr__(sub_key, attrs[sub_key])
        profile.save(update_fields=update_fields)
        return profile


class UserResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResource
        fields = [
            'oil',
            'ammo',
            'steel',
            'aluminium',
            'dd_cube',
            'cl_cube',
            'bb_cube',
            'cv_cube',
            'ss_cube',
            'fast_repair',
            'fast_build',
            'build_map',
            'equipment_map',
        ]
