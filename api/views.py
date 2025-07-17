from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from djoser.views import UserViewSet as DjoserUserViewSet
from django.db import transaction

from .serializers import AvatarSerializer, AvatarReadOnlySerializer
from .tasks import delete_image_s3

from users.models import Avatar, UserProfile


class ProfileViewSet(DjoserUserViewSet):

    @action(
        methods=['post'],
        detail=False,
        url_path='me/avatar',
        permission_classes=[permissions.IsAuthenticated],
    )
    def me_avatar(self, request):
        serializer = AvatarSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @me_avatar.mapping.get
    def get_list_avatar(self, request):
        user = (
            UserProfile.objects
            .prefetch_related('avatars')
            .get(id=request.user.id)
        )
        avatars = user.avatars.all()
        serializer = AvatarReadOnlySerializer(avatars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    @me_avatar.mapping.patch
    def put_active_avatar(self, request):
        user = self.get_instance()
        avatar_id = request.data.get('id')
        if not avatar_id:
            raise ValidationError('Поле id обязателено')

        avatar = get_object_or_404(Avatar, id=avatar_id, user=user)

        if user.active_avatar:
            user.active_avatar.active = False
            user.active_avatar.save()

        avatar.active = True
        avatar.save()
        serializer = AvatarReadOnlySerializer(avatar)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    @action(
        methods=['delete'],
        detail=False,
        url_path=r'me/avatar/(?P<id>\d+)'
    )
    def destroy_avatar(self, request, id=None):
        avatar = get_object_or_404(Avatar, id=id, user=request.user)
        file_path = avatar.image.name
        avatar.delete()
        delete_image_s3.delay_on_commit(file_path)
        return Response(status=status.HTTP_204_NO_CONTENT)
