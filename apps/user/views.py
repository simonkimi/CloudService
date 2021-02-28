from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from .models import User
from .serializers import UserLoginSerializer, UserRegisterSerializer, UserSerializer


class UserViewSets(GenericViewSet):
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication]

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

    @action(methods=['GET'], detail=False)
    def mine(self, request):
        user: User = request.user
        serializers = self.get_serializer(user)
        return Response(serializers.data)

    def get_serializer_class(self):
        if self.action in ['login']:
            return UserLoginSerializer
        elif self.action in ['register']:
            return UserRegisterSerializer
        elif self.action in ['mine']:
            return UserSerializer
        return UserLoginSerializer

    def get_permissions(self):
        if self.action in ['mine']:
            return [IsAuthenticated()]
        return [AllowAny()]
