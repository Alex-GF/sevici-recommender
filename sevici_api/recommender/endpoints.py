from rest_framework import permissions, status
from rest_framework.response import Response
from data_manager.models import Station, StationStatus
from rest_framework.decorators import api_view, permission_classes
from data_manager.models import Station
from data_manager.models import StationStatus
from .serializers import StationPredictorSerializer
from django.utils import timezone
from sklearn.linear_model import LinearRegression

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def bikes_predictors_regression(request):
    station_number = request.query_params.get('stationNumber', None)
    date = request.query_params.get('date', None)
    hour = request.query_params.get('hour', None)
    location = request.query_params.get('location', None)
    
    if station_number is None:
        return Response({"error": "You have to provide a stationNumber"}, status=status.HTTP_400_BAD_REQUEST)
    
    if hour is None:
        return Response({"error": "You have to provide an hour"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not date:
        return Response({"error": "You have to provide a date"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            parsed_date = timezone.datetime.strptime(date+" "+hour, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return Response({"error": "The date or hour format is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    
    station_status_progression = StationStatus.objects.filter(station__number=station_number, last_updated__lte=parsed_date, last_updated__gte=parsed_date-timezone.timedelta(days=30)).order_by('last_updated')
    function_points = [{"x": s.last_updated.timestamp(), "y": s.available_bikes} for s in station_status_progression]
    
    bikes_predicted, regression_function_parameters = _linear_regresion_predictor(parsed_date, station_status_progression)
    
    yourdata= {"bikes_predicted": bikes_predicted, "evolution": function_points, "linear_function": regression_function_parameters,"station": station_status_progression[0].station}
    results = StationPredictorSerializer(yourdata).data
    return Response(results, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def bikes_predictors_mean(request):
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

def _linear_regresion_predictor(parsed_date, station_status_progression):
    
    origin_timestamp = station_status_progression[0].last_updated.timestamp()
    
    function_points = [(s.available_bikes, s.last_updated.timestamp()-origin_timestamp) for s in station_status_progression]
    
    linear_regressor = LinearRegression()
    
    linear_regressor.fit([[x[1]] for x in function_points], [x[0] for x in function_points])
    
    print(linear_regressor.coef_[0])
    print(linear_regressor.intercept_)
    
    linear_regresion_ecuation_coef = linear_regressor.coef_[0]
    linear_regresion_ecuation_intercept = linear_regressor.intercept_
    
    print(linear_regresion_ecuation_coef)
    print(linear_regresion_ecuation_intercept)
    
    return (int(linear_regresion_ecuation_coef*(parsed_date.timestamp()-origin_timestamp)+linear_regresion_ecuation_intercept), {
        "coef": linear_regresion_ecuation_coef,
        "intercept": linear_regresion_ecuation_intercept,
    })
    
    