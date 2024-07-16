# models.py
from django.db import models

class Register(models.Model):
    email_id = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    confirm_password = models.CharField(max_length=128)
    activation = models.BooleanField(default=True)
    ip = models.GenericIPAddressField()
    date = models.DateTimeField(auto_now_add=True)
    fingerprint = models.TextField()

class Login(models.Model):
    email_id = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    activation = models.BooleanField(default=True)
