from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Station, StationStatus
from .serializers import UserSerializer, StationSerializer, StationStatusSerializer
from django.utils import timezone
from rest_framework import generics

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class StationStatusViewSet(generics.ListAPIView):
    serializer_class = StationStatusSerializer
    
    def get_queryset(self):
        date = self.request.query_params.get('date')
        hour = self.request.query_params.get('hour')
        if not hour:
            hour = "23:59:59"
        try:
            if not date:
                parsed_date = timezone.now()
            else:
                parsed_date = timezone.datetime.strptime(date+" "+hour, "%Y-%m-%d %H:%M:%S")
            return StationStatus.objects.filter(id__in=[StationStatus.objects.filter(station__number=station.number, last_updated__lte=parsed_date).last().id for station in Station.objects.all()])
        except AttributeError:
            return StationStatus.objects.none()