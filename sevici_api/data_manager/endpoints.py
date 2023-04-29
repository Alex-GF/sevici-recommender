from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Station, StationStatus
from .serializers import UserSerializer, StationSerializer, StationStatusSerializer
from rest_framework.decorators import api_view

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class StationStatusViewSet(viewsets.ModelViewSet):
    queryset = StationStatus.objects.all()
    serializer_class = StationStatusSerializer