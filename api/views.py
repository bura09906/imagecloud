from rest_framework import status, viewsets
from rest_framework.response import Response

from avatar.models import Avatar

from .serializers import AvatarSerializer


class AvatarViewSet(viewsets.ModelViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.image.delete(save=False)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
