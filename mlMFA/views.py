from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render, get_object_or_404
from .models import Finger
from django.contrib.auth.models import User
from .serializers import UserSerializer, FingerprintSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class FingerprintViewSet(viewsets.ModelViewSet):
    queryset = Finger.objects.all()
    serializer_class = FingerprintSerializer

    @action(detail=True, methods=['post'])
    def upload_fingerprint(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = FingerprintSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def visualize_fingerprints(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        fingerprints = Finger.objects.filter(user=user)
        return render(request, 'visualize_fingerprints.html', {'user': user, 'fingerprints': fingerprints})
