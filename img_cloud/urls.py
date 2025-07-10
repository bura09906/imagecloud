from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import AvatarViewSet

router = SimpleRouter()
router.register('avatar', AvatarViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
