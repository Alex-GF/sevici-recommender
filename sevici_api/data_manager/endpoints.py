from rest_framework import viewsets
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Station, StationStatus
from .serializers import UserSerializer, StationStatusSerializer
from django.utils import timezone
from rest_framework import generics
from .pagination import LargePaginationResult

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
        try:
            if not date:
                parsed_date = timezone.now()
            else:
                parsed_date = timezone.datetime.strptime(date+" "+hour, "%Y-%m-%d %H:%M:%S")
            station_status_on_given_time = StationStatus.objects.filter(id__in=[StationStatus.objects.filter(station__number=station.number, last_updated__lte=parsed_date).last().id for station in Station.objects.all()])

            query = Q()

            if wanted_available_bikes and wanted_available_bikes < 0:
                return StationStatus.objects.none()
            elif wanted_available_bikes:
                query &= Q(available_bikes__gte=wanted_available_bikes)

            if wanted_total_bikes and wanted_total_bikes < 0:
                return StationStatus.objects.none()
            elif wanted_total_bikes:
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