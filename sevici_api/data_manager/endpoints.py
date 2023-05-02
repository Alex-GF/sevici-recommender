from rest_framework import viewsets
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Station, StationStatus
from .serializers import UserSerializer, StationStatusSerializer
from django.utils import timezone
from rest_framework import generics
from .pagination import LargePaginationResult
import re

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class StationStatusViewSet(generics.ListAPIView):
    serializer_class = StationStatusSerializer
    pagination_class = LargePaginationResult
    
    def get_queryset(self):
        date = self.request.query_params.get('date', None)
        hour = self.request.query_params.get('hour', None)
        wanted_available_bikes = int(self.request.query_params.get('available-bikes', 0))
        wanted_total_bikes = int(self.request.query_params.get('station-capacity', 0))
        wanted_station_status = self.request.query_params.get('station-status', None)

        if not hour:
            hour = "23:59:59"
        if not re.match(r"^(((([0-1][0-9])|(2[0-3])):[0-5][0-9]:[0-5][0-9]+$))", hour):
            raise ValueError("Hour must be in format HH:MM:SS")
        try:
            if not date:
                parsed_date = timezone.now()
            else:
                if not re.match(r"^^(((([2][0][2][0-9]))):([0][0-9]|[1][0-2]):([0-2][0-9]|[3][0-1])+$))", date):
                    raise ValueError("Date must be in format YYYY-MM-DD")
                parsed_date = timezone.datetime.strptime(date+" "+hour, "%Y-%m-%d %H:%M:%S")
            station_status_on_given_time = StationStatus.objects.filter(id__in=[StationStatus.objects.filter(station__number=station.number, last_updated__lte=parsed_date).last().id for station in Station.objects.all()])

            query = Q()

            if wanted_available_bikes:
                if wanted_available_bikes < 0:
                    raise ValueError("Available bikes must be a positive integer")
                query &= Q(available_bikes__gte=wanted_available_bikes)

            if wanted_total_bikes:
                if wanted_total_bikes < 0:
                    raise ValueError("Total bikes must be a positive integer")
                query &= Q(total_capacity__gte=wanted_total_bikes)

            if wanted_station_status:

                parsed_stations_status = _parse_station_status(wanted_station_status)

                if parsed_stations_status is not None and parsed_stations_status:
                    query &= Q(is_open=True)
                elif parsed_stations_status is not None and not parsed_stations_status:
                    query &= Q(is_open=False)

            return station_status_on_given_time.filter(query)


        except AttributeError:
            return StationStatus.objects.none()
        
# ------------------------------ PRIVATE METHODS ------------------------------ #

def _parse_station_status(wanted_station_status):

    if wanted_station_status == "Abierta":
        return True
    elif wanted_station_status == "Cerrada":
        return False
    else:
        return None