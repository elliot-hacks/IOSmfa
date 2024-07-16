from django.urls import path
from . import views

urlpatterns = [
    path('capture_fingerprint/', views.capture_fingerprint, name='capture_fingerprint'),
    path('match_fingerprint/', views.match_fingerprint, name='match_fingerprint'),
    path('devices/', views.device_list_create, name='device_list_create'),
    path('devices/<int:pk>/', views.device_detail, name='device_detail'),
]
