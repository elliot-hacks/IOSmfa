# forms.py
from django import forms
from .models import Register

class RegisterForm(forms.ModelForm):
    exampleInputPassword2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    
    class Meta:
        model = Register
        fields = ['email_id', 'password', 'confirm_password', 'fingerprint']
        widgets = {
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("exampleInputPassword2")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
