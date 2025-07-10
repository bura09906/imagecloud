import pytest
from dotenv import load_dotenv
from PIL import Image
from rest_framework import status

from avatar.models import Avatar

load_dotenv()


@pytest.mark.django_db
def test_create_avatar_image(create_avatar_db):
    response = create_avatar_db
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_avatar_exists(create_avatar_db):
    create_avatar_db
    assert Avatar.objects.filter(name="test-avatar").exists()


@pytest.mark.django_db
def test_size_image(create_avatar_db):
    create_avatar_db
    avatar = Avatar.objects.filter(name="test-avatar").first()
    image_file = avatar.image.open()
    img = Image.open(image_file)
    width, height = img.size
    assert width == height
    assert width < 1024 and height < 768
