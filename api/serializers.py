from rest_framework import serializers
from djoser.serializers import UserSerializer as DjoserUserSerializer
from api.utils import ImageProcessor
from users.models import UserProfile, Avatar


class AvatarSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Avatar
        fields = ('user', 'image',)

    def process_image(self, user, image):
        return ImageProcessor(user=user, image=image).process()

    def create(self, validated_data):
        user = validated_data['user']
        image = validated_data['image']

        processed_file = self.process_image(user, image)

        validated_data['image'] = processed_file
        validated_data['active'] = True
        return super().create(validated_data)


class ProfileSerializer(DjoserUserSerializer):
    avatars = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = DjoserUserSerializer.Meta.fields + ('avatars',)
        read_only_fields = fields

    def get_avatars(self, obj):
        avatar = obj.active_avatar
        if avatar:
            serializer = AvatarSerializer(avatar)
            return serializer.data


class AvatarReadOnlySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Avatar
        fields = ('id', 'image', 'user')
        read_only_fields = ('id', 'image', 'user')
