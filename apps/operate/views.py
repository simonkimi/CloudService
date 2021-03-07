from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from utils.pagination import StanderPageNumberPagination
from .models import OperateModel
from .serializers import OperateListSerializers


class OperateViewSets(ListModelMixin, GenericViewSet):
    serializer_class = OperateListSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StanderPageNumberPagination

    def get_queryset(self):
        return OperateModel.objects.filter(user=self.request.user).order_by('-create_time')
