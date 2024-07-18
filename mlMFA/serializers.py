from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Finger

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class FingerprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finger
        fields = ['id', 'user', 'image', 'uploaded_at']
