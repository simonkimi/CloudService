from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.pagination import StanderPageNumberPagination
from .models import ExploreModel
from .serializers import ExploreListSerializer, StatisticSerializer


class ExploreViewSet(ListModelMixin, GenericViewSet):
    pagination_class = StanderPageNumberPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExploreModel.objects.filter(user=self.request.user).order_by('-create_time')

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
            return ExploreListSerializer
        return StatisticSerializer
