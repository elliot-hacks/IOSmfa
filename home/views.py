# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .forms import RegisterForm
from .models import Register, Login
from .utils import encrypt
import hashlib

# Create your views here.




from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def user_login(request):
    if request.method == 'POST' and 'submit' in request.POST:
        fingerprint_matched = request.POST.get('fingerprint_matched', '0')
        if fingerprint_matched == '1':
            return redirect('next_page_url')  # Change 'next_page_url' to the appropriate URL

    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        'fingerprint': user_profile.fingerprint,
    }
    return render(request, 'user_login.html', context)

@login_required
def get_fingerprint(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return JsonResponse({'fingerprint': user_profile.fingerprint})


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
