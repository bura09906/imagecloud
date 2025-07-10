import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from dotenv import load_dotenv
from PIL import Image
from rest_framework.test import APIClient


load_dotenv()


@pytest.fixture()
def get_api_client():
    return APIClient()


@pytest.fixture()
def create_image_file():
    image = Image.new('RGB', (1024, 768), color='red')
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    buffer.seek(0)

    return SimpleUploadedFile(
        name='test.jpg',
        content=buffer.read(),
        content_type='image/jpeg'
    )


@pytest.fixture()
def create_avatar_db(
    get_api_client,
    create_image_file,
):
    response = get_api_client.post('/avatar/', {
        'name': 'test-avatar',
        'image': create_image_file,
    }, format='multipart')

    yield response
