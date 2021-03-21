from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.pagination import StanderPageNumberPagination

from .models import CampaignModel
from .serializers import CampaignSerializer, StatisticSerializer


class CampaignViewSet(ListModelMixin, GenericViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StanderPageNumberPagination

    def get_queryset(self):
        return CampaignModel.objects.filter(user=self.request.user).order_by('-create_time')

    @action(methods=['GET'], detail=False)
    def statistic(self, request):
        serializer = self.get_serializer(data=request.GET, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.save(),
            status=status.HTTP_200_OK
        )

    def get_serializer_class(self):
        if self.action in ['list']:
            return CampaignSerializer
        return StatisticSerializer
