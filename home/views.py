# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Register, Login
from .utils import encrypt
import hashlib
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


def remove_user_and_redirect(request):
    User.objects.filter(username=request.user.username).delete()
    logout(request)
    messages.error(request, f'Your fingerprint capture was not valid. Kindly re-register and try again.')
    return redirect(reverse('accounts:register'))
