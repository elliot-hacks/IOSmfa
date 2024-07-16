from rest_framework import serializers
from home.models import User, Finger, Device, Log

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

class FingerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finger
        fields = ['id', 'username', 'finger_id', 'finger_data']

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'device_name', 'sn', 'vc', 'ac', 'vkey']

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['id', 'username', 'log_time', 'data']
