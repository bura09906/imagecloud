from django.conf import settings
from django.db import models


class Avatar(models.Model):
    name = models.CharField(
        max_length=settings.DB_MAX_LEN_NAME_FEILD,
        unique=True
    )
    image = models.ImageField()
