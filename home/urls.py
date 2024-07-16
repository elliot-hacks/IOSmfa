from django.urls import path
from . import views

urlpatterns = [
    path('fingerprint_scan/', views.fingerprint_scan, name='fingerprint_scan'),
    path('match_fingerprint/', views.match_fingerprint, name='match_fingerprint'),
    path('capture_fingerprint/', views.capture_fingerprint, name='capture_fingerprint'),
]
