from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from utils.pagination import StanderPageNumberPagination
from .models import RepairModel
from .serializers import RepairSerializer


class RepairViewSet(ListModelMixin, GenericViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StanderPageNumberPagination
    serializer_class = RepairSerializer

    def get_queryset(self):
        return RepairModel.objects.filter(user=self.request.user)
