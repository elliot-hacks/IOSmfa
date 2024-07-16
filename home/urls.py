from django.urls import path
from . import views

urlpatterns = [
    path('fingerprint_scan/', views.fingerprint_scan, name='fingerprint_scan'),
    path('match_fingerprint/', views.match_fingerprint, name='match_fingerprint'),
    path('capture_fingerprint/', views.capture_fingerprint, name='capture_fingerprint'),
    # Devices urls
    path('', views.read, name='device-read'),
    path('create_device', views.create_device, name='device-create'),
    path('update_device/<int:id_device>', views.update_device, name='device-update'),
    path('delete_device/<int:id_device>', views.delete_device, name='device-delete'),
    path('getac_device', views.getac_device, name='getac-device'),
    # Log URLS
    path('logs', views.log_index, name='log-index'),
    path('message', views.log_message, name='log-message'),
    # User urls
    path('create_user', views.create_user, name='user-create'),
    path('read_user', views.read_user, name='user-read'),
    path('update_user/<int:id_user>', views.update_user, name='user-update'),
    path('delete_user/<int:id_user>', views.delete_user, name='user-delete'),
    path('register', views.user_register, name='user-register'),
    path('register/process', views.process_register, name='process-register'),
    path('verification', views.user_verification, name='user-verification'),
    path('verification/process', views.process_verification, name='process-verification')
]
