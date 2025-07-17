from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ProfileViewSet

router = DefaultRouter()
router.register('users', ProfileViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('users/', include('djoser.urls.jwt')),
]
