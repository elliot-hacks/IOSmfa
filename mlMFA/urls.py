from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, FingerprintViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'fingerprints', FingerprintViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
