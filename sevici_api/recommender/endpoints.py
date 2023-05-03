from rest_framework import permissions, status
from rest_framework.response import Response
from data_manager.models import Station, StationStatus
from rest_framework.decorators import api_view, permission_classes
from data_manager.models import Station
from data_manager.models import StationStatus
from .serializers import StationPredictorLinearSerializer, StationPredictorMeanSerializer
from django.utils import timezone
from sklearn.linear_model import LinearRegression
import itertools

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
    results = StationPredictorLinearSerializer(yourdata).data
    return Response(results, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def bikes_predictors_mean(request):
    #stationNumber param
    station_number_param = request.query_params.get('stationNumber', None)
    if not station_number_param or not Station.objects.filter(number=station_number_param).exists():
        return Response({"error": "You have to provide a valid stationNumber"}, status=status.HTTP_400_BAD_REQUEST)
    station = Station.objects.get(number=station_number_param)
    
    #date param
    date_param = request.query_params.get('date', None)
    if not date_param:
        return Response({"error": "You have to provide a date"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        date = timezone.datetime.strptime(date_param, "%Y-%m-%d")
    except ValueError:
        return Response({"error": "The date format is incorrect. It must be in format YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)
    
    #hour param
    hour_param = request.query_params.get('hour', None)
    if not hour_param:
        return Response({"error": "You have to provide an hour"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        date = timezone.datetime.strptime(date_param+" "+hour_param, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return Response({"error": "The hour format is incorrect. It must be in format HH:MM:SS"}, status=status.HTTP_400_BAD_REQUEST)
    
    is_future = date-timezone.datetime.now()

    if is_future != abs(is_future):
        return Response({"error": "You can't predict the past"}, status=status.HTTP_400_BAD_REQUEST)
    
    mean_prediction = _mean_predictor(station, date.date(), date.time())
    
    station_status_progression = StationStatus.objects.filter(station__number=station_number_param, last_updated__lte=date, last_updated__gte=date-timezone.timedelta(days=30)).order_by('last_updated')
    function_points = [{"x": s.last_updated.timestamp(), "y": s.available_bikes} for s in station_status_progression]

    response_data = {"prediction": [date.timestamp(), mean_prediction], "evolution": function_points, "station": station}
    
    result = StationPredictorMeanSerializer(response_data).data
    return Response(result, status=status.HTTP_200_OK)



def _mean_predictor(station, date, hour):
    max_date = date-timezone.timedelta(days=30)
    station_status_all = StationStatus.objects.filter(station=station, last_updated__gte=max_date)
    station_status_minor = station_status_all.filter(last_updated__time__lte=hour).order_by("-last_updated__time")
    station_status_major = station_status_all.filter(last_updated__time__gte=hour).order_by("last_updated__time")
    
    last_dates = set()
    bikes = 0
    total = 0
    
    for ss_minor, ss_major in itertools.zip_longest(station_status_minor, station_status_major):
        if ss_minor is None:
            ss_minor = ss_major
        if ss_major is None:
            ss_major = ss_minor
        tuple_date = (ss_minor.last_updated.day, ss_minor.last_updated.month, ss_minor.last_updated.year)
        if tuple_date not in last_dates:
            last_dates.add(tuple_date)
            bikes += round((ss_minor.available_bikes+ss_major.available_bikes)/2)
            total += 1
            
   
    penalization = abs((date-timezone.now().date()).days)
    
    avg = round((bikes/total)*(1-penalization*(0.05))) if total else 0
    

    return avg

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
    
    