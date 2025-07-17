from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image


class ImageProcessor:

    def __init__(self, user, image, size=512, quality=85):
        self.avatar_user = user
        self.image = image
        self.size = size
        self.quality = quality

    def open_file(self):
        return Image.open(self.image)

    def crop_center_square(self, img):
        width, height = img.size

        if width == height:
            return img

        min_dim = min(width, height)
        left = (width - min_dim) / 2
        top = (height - min_dim) / 2
        right = left + min_dim
        bottom = top + min_dim
        return img.crop((left, top, right, bottom))

    def resize_image(self, img):
        return img.resize((self.size, self.size), Image.Resampling.LANCZOS)

    def process(self):
        img = self.open_file()
        img = self.crop_center_square(img)
        img = self.resize_image(img)
        img = img.convert("RGB")
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=self.quality)
        return ContentFile(buffer.getvalue(), name=f'{self.avatar_user}.jpg')
