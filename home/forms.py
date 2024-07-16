# forms.py
from django import forms
from .models import Device, UserProfile

# class RegisterForm(forms.ModelForm):
#     exampleInputPassword2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    
#     class Meta:
#         model = Register
#         fields = ['email_id', 'password', 'confirm_password', 'fingerprint']
#         widgets = {
#             'password': forms.PasswordInput(),
#             'confirm_password': forms.PasswordInput(),
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("exampleInputPassword2")

#         if password != confirm_password:
#             raise forms.ValidationError("Passwords do not match.")

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
            'device_name': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'placeholder': 'Enter Name',
                }
            ),
            'sn': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'placeholder': 'Enter SN'
                }
            ),
            'vc': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'placeholder': 'Enter VC'
                }
            ),
            'ac': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'placeholder': 'Enter AC'
                }
            ),
            'vkey': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'placeholder': 'Enter VKEY'
                }
            )
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
        model = UserProfile
        fields = [
            'username',
        ]
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'placeholder': 'Enter Username'
                }
            )
        }
