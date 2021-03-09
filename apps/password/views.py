from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import PasswordModel
from .serializers import ActiveSerializers


class PasswordViewSet(GenericViewSet):
    queryset = PasswordModel.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = ActiveSerializers

    @action(methods=['POST'], detail=False)
    def active(self, request):
        serializers = self.get_serializer(data=request.data, context={'user': request.user})
        serializers.is_valid(raise_exception=True)
        profile = serializers.save()
        return Response(profile)
