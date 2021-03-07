from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import PvpModel
from .serializers import PvpListSerializer
from utils.pagination import StanderPageNumberPagination


class PvpViewSet(ListModelMixin, GenericViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StanderPageNumberPagination
    serializer_class = PvpListSerializer

    def get_queryset(self):
        return PvpModel.objects.filter(user=self.request.user).order_by('-create_time')
