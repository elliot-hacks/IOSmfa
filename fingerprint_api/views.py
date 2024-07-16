from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.models import User, Finger, Device, Log
from .serializers import UserSerializer, FingerSerializer, DeviceSerializer, LogSerializer
from home.mantra_sdk import MantraSDK

sdk = MantraSDK()

@api_view(['POST'])
def capture_fingerprint(request):
    quality = request.data.get('quality', 60)
    timeout = request.data.get('timeout', 10)

    response = sdk.capture_finger(quality, timeout)
    if response['httpStatus']:
        return Response({'status': 'success', 'data': response['data']}, status=status.HTTP_200_OK)
    return Response({'status': 'error', 'message': 'HTTP request failed', 'error': response['err']}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def match_fingerprint(request):
    quality = request.data.get('quality', 60)
    timeout = request.data.get('timeout', 10)
    fingerprint_template = request.data.get('fingerprint_template')

    response = sdk.match_finger(quality, timeout, fingerprint_template)
    if response['httpStatus']:
        if response['data']['Status']:
            return Response({'status': 'success', 'message': 'Fingerprint matched'}, status=status.HTTP_200_OK)
        return Response({'status': 'failure', 'message': 'Fingerprint not matched', 'error': response['data']['ErrorDescription']}, status=status.HTTP_200_OK)
    return Response({'status': 'error', 'message': 'HTTP request failed', 'error': response['err']}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def device_list_create(request):
    if request.method == 'GET':
        devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def device_detail(request, pk):
    try:
        device = Device.objects.get(pk=pk)
    except Device.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DeviceSerializer(device)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = DeviceSerializer(device, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        device.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
