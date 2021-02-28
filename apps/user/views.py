from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from .models import User
from .serializers import UserLoginSerializer, UserRegisterSerializer


class UserViewSetMixin(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = User.objects.all()

    @action(methods=['POST'], detail=False)
    def login(self, request):
        user: User = request.user
        if not user.is_authenticated:
            return Response(data={'error': '请登录'}, status=status.HTTP_401_UNAUTHORIZED)
        serializers = UserLoginSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        token = serializers.save()
        return Response({'token': token})

    @action(methods=['POST'], detail=False)
    def register(self, request):
        serializers = UserRegisterSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        token = serializers.save()
        return Response({'token': token})

    @action(methods=['POST'], detail=False)
    def mine(self, request):
        user: User = request.user
        if not user.is_authenticated:
            return Response(data={'error': '请登录'}, status=status.HTTP_401_UNAUTHORIZED)
        serializers = UserRegisterSerializer(user)
        return serializers.data
