from django.db.models import Q
from .models import Station, StationStatus
from .serializers import StationStatusSerializer
from django.utils import timezone
from rest_framework import generics
from .pagination import LargePaginationResult
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance 
from django.contrib.gis.db.models.functions import Distance as DistanceFunc
import pytz

class StationStatusViewSet(generics.ListAPIView):
    serializer_class = StationStatusSerializer
    pagination_class = LargePaginationResult
    
    def get_queryset(self):
        date = self.request.query_params.get('date', None)
        hour = self.request.query_params.get('hour', None)
        wanted_available_bikes = self.request.query_params.get('availableBikes', 0)
        wanted_total_bikes = self.request.query_params.get('stationCapacity', 0)
        wanted_station_status = self.request.query_params.get('stationStatus', None)
        station_number = self.request.query_params.get('stationNumber', None)
        
        try:
            wanted_available_bikes = int(wanted_available_bikes)
        except ValueError:
            raise ValueError("Available bikes must be an integer")
        
        try:
            wanted_total_bikes = int(wanted_total_bikes)
        except ValueError:
            raise ValueError("Total bikes must be an integer")
        
        if station_number:
            try:
                station_number = int(station_number)
            except ValueError:
                raise ValueError("Station number must be an integer")
        
        if not hour:
            hour = "23:59:59"
        
        if not date:
            parsed_date = timezone.make_aware(timezone.datetime.now(), timezone=pytz.utc)
        else:
            try:
                parsed_date = timezone.make_aware(timezone.datetime.strptime(date+" "+hour, "%Y-%m-%d %H:%M:%S"), timezone=timezone.get_current_timezone())-timezone.timedelta(hours=2)
            except ValueError:
                raise ValueError("Incorrect date or time format, should be YYYY-MM-DD and HH:MM:SS")
            
        is_future = parsed_date-timezone.make_aware(timezone.datetime.now(), timezone=pytz.utc)

        if is_future == abs(is_future):
            raise ValueError("You can't show the future, Marty!")
        
        station_status_on_given_time = StationStatus.objects.filter(id__in=[StationStatus.objects.filter(station__number=station.number, last_updated__lte=parsed_date).last().id for station in Station.objects.all() if StationStatus.objects.filter(station__number=station.number, last_updated__lte=parsed_date).exists()])

        query = Q()

        if wanted_available_bikes:
            if wanted_available_bikes < 0:
                raise ValueError("Available bikes must be a positive integer")
            query &= Q(available_bikes__gte=wanted_available_bikes)

        if wanted_total_bikes:
            if wanted_total_bikes < 0:
                raise ValueError("Total bikes must be a positive integer")
            query &= Q(total_capacity__gte=wanted_total_bikes)
            
        if station_number:
            if station_number < 0:
                raise ValueError("Station number must be a positive integer")
            query &= Q(station__number=station_number)

        if wanted_station_status:

            parsed_stations_status = _parse_station_status(wanted_station_status.lower().strip())

            if parsed_stations_status is not None and parsed_stations_status:
                query &= Q(is_open=True)
            elif parsed_stations_status is not None and not parsed_stations_status:
                query &= Q(is_open=False)

        return station_status_on_given_time.filter(query)

class StationStatusNearbyViewSet(generics.ListAPIView):
    serializer_class = StationStatusSerializer
    pagination_class = LargePaginationResult
    
    def get_queryset(self):
        date = self.request.query_params.get('date', None)
        hour = self.request.query_params.get('hour', None)
        wanted_available_bikes = self.request.query_params.get('availableBikes', 0)
        wanted_total_bikes = self.request.query_params.get('stationCapacity', 0)
        wanted_station_status = self.request.query_params.get('stationStatus', None)
        
        limit = self.request.query_params.get('limit', None)
        
        latitude_param = self.request.query_params.get('latitude', None)
        if not latitude_param:
            raise ValueError("You have to provide a latitude")
        try :
            latitude = float(latitude_param)
        except ValueError:
            raise ValueError("The latitude format is incorrect")
        
        longitude_param = self.request.query_params.get('longitude', None)
        if not longitude_param:
            return ValueError("You have to provide a longitude")
        try:
            longitude = float(longitude_param)
        except ValueError:
            return ValueError("The longitude format is incorrect")
        
        radius_param = self.request.query_params.get('radius', None)
        if not radius_param:
            raise ValueError("You have to provide a radius")
        try:
            radius = float(radius_param)
        except ValueError:
            raise ValueError("The radius format is incorrect")
        if radius < 0:
            raise ValueError("The radius must be positive")
        
        location = Point(longitude, latitude)
        
        try:
            wanted_available_bikes = int(wanted_available_bikes)
        except ValueError:
            raise ValueError("Available bikes must be an integer")
        
        try:
            wanted_total_bikes = int(wanted_total_bikes)
        except ValueError:
            raise ValueError("Total bikes must be an integer")
        
        if limit:
            try:
                limit = int(limit)
            except ValueError:
                raise ValueError("Limit must be an integer")
            if limit < 0:
                raise ValueError("Limit must be a positive integer")
        
        if not hour:
            hour = "23:59:59"
        
        if not date:
            parsed_date = timezone.make_aware(timezone.datetime.now(), timezone=pytz.utc)
        else:
            try:
                parsed_date = timezone.make_aware(timezone.datetime.strptime(date+" "+hour, "%Y-%m-%d %H:%M:%S"), timezone=timezone.get_current_timezone())-timezone.timedelta(hours=2)
            except ValueError:
                raise ValueError("Incorrect date or time format, should be YYYY-MM-DD and HH:MM:SS")
            
        is_future = parsed_date-timezone.make_aware(timezone.datetime.now(), timezone=pytz.utc)

        if is_future == abs(is_future):
            raise ValueError("You can't show the future, Marty!")
        
        station_status_on_given_time = StationStatus.objects.filter(id__in=[StationStatus.objects.filter(station__number=station.number, last_updated__lte=parsed_date).last().id for station in Station.objects.filter(location__distance_lt=(location, Distance(km=radius))).annotate(distance=DistanceFunc("location", location)).order_by("distance") if StationStatus.objects.filter(station__number=station.number, last_updated__lte=parsed_date).exists()])

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

            parsed_stations_status = _parse_station_status(wanted_station_status.lower().strip())

            if parsed_stations_status is not None and parsed_stations_status:
                query &= Q(is_open=True)
            elif parsed_stations_status is not None and not parsed_stations_status:
                query &= Q(is_open=False)

        result = station_status_on_given_time.filter(query)
        if limit:
            result = result[:limit]
        
        return result     
        
# ------------------------------ PRIVATE METHODS ------------------------------ #

def _parse_station_status(wanted_station_status):

    if wanted_station_status == "abierta":
        return True
    elif wanted_station_status == "cerrada":
        return False
    elif wanted_station_status == "cualquiera":
        return None
    else:
        raise ValueError("Station status must be 'abierta', 'cerrada' or 'cualquiera'")