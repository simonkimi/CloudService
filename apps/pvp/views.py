from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import PvpModel
from .serializers import PvpListSerializer, StatisticSerializer
from utils.pagination import StanderPageNumberPagination


class PvpViewSet(ListModelMixin, GenericViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StanderPageNumberPagination

    @action(methods=['GET'], detail=False)
    def statistic(self, request):
        serializer = self.get_serializer(data=request.GET, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.save(),
            status=status.HTTP_200_OK
        )

    def get_queryset(self):
        return PvpModel.objects.filter(user=self.request.user).order_by('-create_time')

    def get_serializer_class(self):
        if self.action in ['list']:
            return PvpListSerializer
        return StatisticSerializer
