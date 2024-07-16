from django import forms
from .models import Device, User

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = [
            'device_name',
            'sn',
            'vc',
            'ac',
            'vkey',
        ]
        widgets = {
            'device_name': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter Name'}),
            'sn': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter SN'}),
            'vc': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter VC'}),
            'ac': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter AC'}),
            'vkey': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter VKEY'}),
        }
        labels = {
            'device_name': 'Device Name',
            'sn': 'Device SN',
            'vc': 'Device VC',
            'ac': 'Device AC',
            'vkey': 'Device VKEY',
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter Username'})
        }
