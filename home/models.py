from django.db import models
from django.contrib.auth.models import User

class Finger(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, related_name='home_user')
    finger_id = models.AutoField(primary_key=True)
    finger_data = models.TextField(max_length=255, null=False, blank=False)

class Device(models.Model):
    device_name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    sn = models.CharField(max_length=50, unique=True, null=False, blank=False)
    vc = models.CharField(max_length=50, unique=True, null=False, blank=False)
    ac = models.CharField(max_length=50, unique=True, null=False, blank=False)
    vkey = models.CharField(max_length=50, unique=True, null=False, blank=False)

class Log(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    log_time = models.DateTimeField(auto_now_add=True)
    data = models.TextField()
