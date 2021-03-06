from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from explore.models import ExploreMemory
from repair.models import RepairMemory
from build_ship.models import BuildShipMemory
from build_equipment.models import BuildEquipmentMemory

from explore.serializers import ExploreMemorySerializer
from repair.serializers import RepairMemorySerializer
from build_ship.serializers import BuildShipMemorySerializer
from build_equipment.serializers import BuildEquipmentMemorySerializer

from .models import User, UserResource
from .serializers import UserLoginSerializer, UserRegisterSerializer, UserSerializer, UserSettingSerializer, \
    UserProfileSerializer, UserResourceSerializer


class UserLoginViewSets(GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @action(methods=['GET'], detail=False)
    def mine(self, request):
        user: User = request.user
        serializers = self.get_serializer(user)
        return Response(serializers.data)

    @action(methods=['POST'], detail=False)
    def setting(self, request):
        serializers = self.get_serializer(data=request.data, context={'user': request.user})
        serializers.is_valid(raise_exception=True)
        profile = serializers.save()
        return Response(UserProfileSerializer(profile).data)

    @action(methods=['GET'], detail=False)
    def dashboard(self, request):
        user = self.request.user
        resource = UserResource.objects.get(user=user)
        explore = ExploreMemory.objects.filter(user=user)
        repair = RepairMemory.objects.filter(user=user)
        build = BuildShipMemory.objects.filter(user=user)
        equipment = BuildEquipmentMemory.objects.filter(user=user)

        return Response({
            'resource': UserResourceSerializer(resource).data,
            'explore': ExploreMemorySerializer(explore, many=True).data,
            'repair': RepairMemorySerializer(repair, many=True).data,
            'build': BuildShipMemorySerializer(build, many=True).data,
            'equipment': BuildEquipmentMemorySerializer(equipment, many=True).data,
        })

    def get_serializer_class(self):
        if self.action in ['mine']:
            return UserSerializer
        elif self.action in ['setting']:
            return UserSettingSerializer


class UserViewSets(GenericViewSet):
    queryset = User.objects.all()

    @action(methods=['POST'], detail=False)
    def login(self, request):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        token = serializers.save()
        return Response({'token': token})

    @action(methods=['POST'], detail=False)
    def register(self, request):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        token = serializers.save()
        return Response({'token': token})

    def get_serializer_class(self):
        if self.action in ['login']:
            return UserLoginSerializer
        elif self.action in ['register']:
            return UserRegisterSerializer
        return UserLoginSerializer
