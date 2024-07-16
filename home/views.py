from django.shortcuts import render
from . import utils

# Create your views here.
def register(request):
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
