from rest_framework import views
from rest_framework.response import Response

from data_manager.models import Station, StationStatus

from .serializers import StationPredictorSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from datetime import datetime
from django.utils import timezone


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def bikes_predictors(request):
    date = timezone.datetime.strptime("2023-05-02"+" "+"17:15:00", "%Y-%m-%d %H:%M:%S")
    yourdata= {"bikes_predicted": _mean_predictor(194, date.date(), date.time()), "station": Station.objects.all()[0]}
    results = StationPredictorSerializer(yourdata).data
    return Response(results, status=status.HTTP_200_OK)

def _mean_predictor(number, date, hour):
    max_date = date-timezone.timedelta(days=30)
    station = Station.objects.get(number=number)
    station_status_all = StationStatus.objects.filter(station=station, last_updated__gte=max_date)
    station_status_minor = station_status_all.filter(last_updated__time__lte=hour).order_by("-last_updated__time")
    station_status_major = station_status_all.filter(last_updated__time__gte=hour).order_by("last_updated__time")

    result = []
    last_dates = set()
    bikes = 0
    total = 0
    for ss_minor, ss_major in zip(station_status_minor, station_status_major):
        tuple_date = (ss_minor.last_updated.day, ss_minor.last_updated.month, ss_minor.last_updated.year)
        if tuple_date not in last_dates:
            last_dates.add(tuple_date)
            bikes += round((ss_minor.available_bikes+ss_major.available_bikes)/2)
            total += 1
            result.append((date, round((ss_minor.available_bikes+ss_major.available_bikes)/2)))
    print(result)
    pen = abs((date-timezone.now().date()).days)

    return round((bikes/total)*(1-pen*(0.05))) if total else 0

def _linear_regresion_predictor():
    pass