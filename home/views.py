from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import register
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import hashlib
from .mantra_sdk import MantraSDK
from .models import Device, User, Finger
from .forms import DeviceForm, UserForm

# Initialize Mantra SDK
sdk = MantraSDK()

# @login_required
def fingerprint_scan(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    context = {
        'fingerprint_template': user_profile.fingerprint_template
    }
    return render(request, 'fingerprint_scan.html', context)

# @login_required
def match_fingerprint(request):
    if request.method == "POST":
        quality = request.POST.get('quality', 60)
        timeout = request.POST.get('timeout', 10)
        fingerprint_template = request.POST.get('fingerprint_template')

        response = sdk.match_finger(quality, timeout, fingerprint_template)
        
        if response['httpStatus']:
            if response['data']['Status']:
                return JsonResponse({'status': 'success', 'message': 'Fingerprint matched'})
            else:
                return JsonResponse({'status': 'failure', 'message': 'Fingerprint not matched', 'error': response['data']['ErrorDescription']})
        else:
            return JsonResponse({'status': 'error', 'message': 'HTTP request failed', 'error': response['err']})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

# @login_required
def capture_fingerprint(request):
    if request.method == "POST":
        quality = request.POST.get('quality', 60)
        timeout = request.POST.get('timeout', 10)

        response = sdk.capture_finger(quality, timeout)
        
        if response['httpStatus']:
            return JsonResponse({'status': 'success', 'data': response['data']})
        else:
            return JsonResponse({'status': 'error', 'message': 'HTTP request failed', 'error': response['err']})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# Devices API
def create_device(request):
    form = DeviceForm()
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/device/')
        else:
            return HttpResponse('Error in forms, click <a href="/device/">here</a> to go back')
    else:
        context = {
            'form': form,
            'menu': 'device'
        }
        return render(request, 'device/form.html', context)


def read_device(request):
    devices = Device.objects.all()
    context = {
        'devices': devices,
        'menu': 'device'
    }
    return render(request, 'device/index.html', context)


def update_device(request, id_device):
    device_id = int(id_device)
    try:
        device = Device.objects.get(id=device_id)
    except Device.DoesNotExist:
        return redirect('/device/')
    form = DeviceForm(request.POST or None, instance=device)
    if form.is_valid():
        form.save()
        return redirect('/device/')
    else:
        context = {
            'form': form,
            'menu': 'device'
        }
        return render(request, 'apps/device/form.html', context)


def delete_device(request, id_device):
    device_id = int(id_device)
    try:
        device = Device.objects.get(id=device_id)
    except Device.DoesNotExist:
        return redirect('/device/')
    device.delete()
    return redirect('/device/')


def getac_device(request):
    vc = request.GET.get('vc')
    try:
        device_acsn = Device.objects.get(vc=vc)
        return HttpResponse(device_acsn.ac + device_acsn.sn)
    except Device.DoesNotExist:
        return HttpResponse('empty')


# Logs
def log_index(request):
    context = {
        'menu': 'log'
    }
    return render(request, 'log/index.html', context)


def log_message(request):
    user_name = request.GET.get('user_name')
    time = request.GET.get('time')
    if user_name is not None and time is not None:
        return HttpResponse(user_name + ' login success on ' + str(datetime.strptime(time, '%Y%m%d%H%M%S')))
    else:
        message = request.GET.get('msg')
        return HttpResponse(message)

# Users
def create_user(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/user/')
        else:
            return HttpResponse('Error in forms, click <a href="/user/">here</a> to go back')
    else:
        context = {
            'form': form,
            'menu': 'user',
        }
        return render(request, 'user/form.html', context)


def read_user(request):
    users = User.objects.all()
    context = {
        'users': users,
        'menu': 'user',
    }
    return render(request, 'user/index.html', context)


def update_user(request, id_user):
    user_id = int(id_user)
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('/user/')
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('/user/')
    else:
        context = {
            'form': form,
            'menu': 'user',
        }
        return render(request, 'user/form.html', context)


def delete(request, id_user):
    user_id = int(id_user)
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('/user/')
    user.delete()
    return redirect('/user/')


def user_register(request):
    baseurl = request.build_absolute_uri('/')
    user_id = request.GET.get('user_id')
    sectkey = 'SecurityKey'
    limit = 15
    result = user_id + ';' + sectkey + ';' + str(limit) + ';' + baseurl + 'user/register/process;' + baseurl + 'device/getac'
    return HttpResponse(result)


@csrf_exempt
def process_register(request):
    reg = request.POST
    data = []
    for r in reg:
        data.append(r)
    data[0] = request.POST.get('RegTemp')
    if data[0] is not None:
        vstamp = data[0]
        sn = data[1]
        user_id = data[2]
        regtemp = data[3]
        try:
            device = Device.objects.get(sn=sn)
        except Device.DoesNotExist:
            device = None
        temp = device.ac + device.vkey + regtemp + sn + user_id
        salt = hashlib.md5(temp.encode('utf-8')).hexdigest()
        if str(vstamp).upper() == str(salt).upper():
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                user = None
            Finger(username=user, finger_data=regtemp).save()
        return HttpResponse('empty')
    else:
        HttpResponse('Parameter invalid..')


def user_verification(request):
    baseurl = request.build_absolute_uri('/')
    user_id = request.GET.get('user_id')
    try:
        finger = Finger.objects.get(username__id=user_id)
    except Finger.DoesNotExist:
        finger = ''
    sectkey = 'SecurityKey'
    limit = 10
    result = user_id + ';' + finger.finger_data + ';' + sectkey + ';' + str(limit) + ';' + baseurl + 'user/verification/process;' + baseurl + 'device/getac;extraParams'
    return HttpResponse(result)


@csrf_exempt
def process_verification(request):
    baseurl = request.build_absolute_uri('/')
    ver = request.POST
    data = []
    for v in ver:
        print(v)
        data.append(v)
    data[0] = request.POST.get('VerPas')
    if data[0] is not None:
        user_id = data[0]
        vstamp = data[1]
        time = data[2]
        sn = data[3]
        try:
            fingerdata = Finger.objects.get(username__id=user_id)
        except Finger.DoesNotExist:
            fingerdata = None
        try:
            device = Device.objects.get(sn=sn)
        except Device.DoesNotExist:
            device = None
        user_name = fingerdata.username.username
        temp = sn + fingerdata.finger_data + device.vc + time + user_id + device.vkey
        salt = hashlib.md5(temp.encode('utf-8')).hexdigest()
        if str(vstamp).upper() == str(salt).upper():
            return HttpResponse(baseurl + 'log/message?user_name=' + user_name + '&time=' + time)
        else:
            return HttpResponse(baseurl + 'log/message?msg=error')
    else:
        msg = 'Parameter invalid..'
        return HttpResponse(msg)


@register.filter(name='finger_template')
def finger_template(value):
    finger = Finger.objects.filter(username__id=value).exists()
    if finger:
        return 1
    else:
        return 0
