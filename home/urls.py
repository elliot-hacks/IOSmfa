from django.urls import path
from . import views

urlpatterns = [
    path('fingerprint_scan/', views.fingerprint_scan, name='fingerprint_scan'),
    path('match_fingerprint/', views.match_fingerprint, name='match_fingerprint'),
    path('capture_fingerprint/', views.capture_fingerprint, name='capture_fingerprint'),
    path('device/', views.read_device, name='device-read'),
    path('device/create/', views.create_device, name='device-create'),
    path('device/update/<int:id_device>/', views.update_device, name='device-update'),
    path('device/delete/<int:id_device>/', views.delete_device, name='device-delete'),
    path('device/getac/', views.getac_device, name='getac-device'),
    path('log/', views.log_index, name='log-index'),
    path('log/message/', views.log_message, name='log-message'),
    path('user/', views.read_user, name='user-read'),
    path('user/create/', views.create_user, name='user-create'),
    path('user/update/<int:id_user>/', views.update_user, name='user-update'),
    path('user/delete/<int:id_user>/', views.delete_user, name='user-delete'),
    path('user/register/', views.user_register, name='user-register'),
    path('user/register/process/', views.process_register, name='process-register'),
    path('user/verification/', views.user_verification, name='user-verification'),
    path('user/verification/process/', views.process_verification, name='process-verification')
]
