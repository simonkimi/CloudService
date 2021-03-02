from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.pagination import StanderPageNumberPagination
from .models import BuildEquipmentModel
from .serializers import BuildEquipmentListSerializer


class BuildEquipmentViewSet(ListModelMixin, GenericViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StanderPageNumberPagination
    serializer_class = BuildEquipmentListSerializer

    def get_queryset(self):
        return BuildEquipmentModel.objects.filter(user=self.request.user)
