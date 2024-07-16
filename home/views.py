# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .forms import RegisterForm
from .models import Register, Login
from .utils import encrypt
import hashlib

# Create your views here.
# utils.py
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import os

ENCRYPTION_KEY = 'd0a7e7997b6d5fcd55f4b5c32611b87cd923e88837b63bf2941ef819dc8ca282'

def encrypt(data):
    key = hashlib.sha256(ENCRYPTION_KEY.encode()).digest()
    iv = os.urandom(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data.encode(), AES.block_size))
    encoded_data = base64.b64encode(encrypted_data).decode('utf-8') + '|' + base64.b64encode(iv).decode('utf-8')
    return encoded_data

def decrypt(encoded_data):
    key = hashlib.sha256(ENCRYPTION_KEY.encode()).digest()
    encoded_data, iv = encoded_data.split('|')
    encrypted_data = base64.b64decode(encoded_data)
    iv = base64.b64decode(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data.decode('utf-8')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email_id']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['exampleInputPassword2']
            fingerprint = form.cleaned_data['fingerprint']

            if Register.objects.filter(email_id=email).exists():
                messages.error(request, "Email already exists.")
            else:
                hashed_password = hashlib.md5(password.encode()).hexdigest()
                ip = request.META.get('REMOTE_ADDR')
                my_date = timezone.now()

                register = Register(
                    email_id=email,
                    password=hashed_password,
                    confirm_password=hashed_password,
                    activation=True,
                    ip=ip,
                    date=my_date,
                    fingerprint=fingerprint
                )
                register.save()

                login = Login(
                    email_id=email,
                    password=hashed_password,
                    activation=True
                )
                login.save()

                messages.success(request, "Successfully Registered!")
                return redirect('login')  # Redirect to login page after successful registration
        else:
            messages.error(request, "Form is not valid. Please check the input.")
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

    if request.method == "POST":
        error = ''
        username = request.POST.get('username').replace('/', '')
        display_name = request.POST.get('display-name')
        if not utils.validate_username(username):
           error = 'Invalid matriculation number'
           return render(request, 'register.html', context = {'page_title': "Register", 'error': error})
        if not utils.validate_display_name(display_name):
           error = 'Invalid display name'
           return render(request, 'register.html', context = {'page_title': "Register", 'error': error})
        if User.objects.filter(username=username).exists():
            error = 'Student already exists.'
            return render(request, 'register.html', context = {'page_title': "Register", 'error': error})
        else:
            u = User.objects.create(first_name = display_name, password='none', is_superuser=False, username=username,  last_name='', display_name=display_name, email='none', is_staff=False, is_active=True,date_joined=timezone.now())
            u.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request,u)
            return redirect(reverse('start_fido2'))
    else:
        return render(request, 'register.html', context = {'page_title': "Register"})
    

def login(request):
    if request.method == "POST":
        username = request.POST.get('username').replace('/', '')
        user = User.objects.filter(username=username).first()
        err=""
        if user is not None:
            if user.is_active:
                if "mfa" in settings.INSTALLED_APPS:
                    from mfa.helpers import has_mfa
                    res =  has_mfa(request,username=username)
                    if res: return res
                    return login_user_in(request, username)
            else:
                err="This student is NOT activated yet."
        else:
            err="No student with such matriculation number exists."
        return render(request, 'login.html', {"err":err})
    else:
        return render(request, 'login.html')


def remove_user_and_redirect(request):
    User.objects.filter(username=request.user.username).delete()
    logout(request)
    messages.error(request, f'Your fingerprint capture was not valid. Kindly re-register and try again.')
    return redirect(reverse('accounts:register'))
