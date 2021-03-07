from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.pagination import StanderPageNumberPagination
from .models import BuildShipModel
from .serializers import BuildShipListSerializer


class BuildShipViewSet(ListModelMixin, GenericViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StanderPageNumberPagination
    serializer_class = BuildShipListSerializer

    def get_queryset(self):
        return BuildShipModel.objects.filter(user=self.request.user).order_by('-create_time')

