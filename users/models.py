from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):

    @property
    def active_avatar(self):
        return self.avatars.filter(active=True).first()


class Avatar(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='avatars'
    )
    image = models.ImageField(blank=True, null=True, unique=True)
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.active:
            Avatar.objects.filter(
                user=self.user, active=True
            ).exclude(id=self.id).update(active=False)
        super().save(*args, **kwargs)
