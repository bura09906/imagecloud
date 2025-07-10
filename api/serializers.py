from rest_framework import serializers

from avatar.models import Avatar
from avatar.utils import ImageProcessor


class AvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Avatar
        fields = ('name', 'image')

    def process_image(self, name, image):
        return ImageProcessor(name=name, image=image).process()

    def create(self, validated_data):
        name = validated_data['name']
        image = validated_data['image']
        processed_file = self.process_image(name, image)
        validated_data['image'] = processed_file
        return super().create(validated_data)

    def update(self, instance, validated_data):
        image = validated_data.get('image', None)

        if image:
            instance.image.delete(save=False)
            name = validated_data.get('name', instance.name)
            processed_file = processed_file = self.process_image(name, image)
            validated_data['image'] = processed_file

        return super().update(instance, validated_data)
