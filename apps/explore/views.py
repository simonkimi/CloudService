from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from utils.pagination import StanderPageNumberPagination
from .models import ExploreModel
from .serializers import ExploreListSerializer, StatisticSerializer


class ExploreViewSet(ListModelMixin, GenericViewSet):
    serializer_class = ExploreListSerializer
    pagination_class = StanderPageNumberPagination

    def get_queryset(self):
        return ExploreModel.objects.filter(user=self.request.user)

    @action(methods=['POST'], detail=False)
    def statistic(self, request):
        serializer = StatisticSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.save(),
            status=status.HTTP_200_OK
        )
