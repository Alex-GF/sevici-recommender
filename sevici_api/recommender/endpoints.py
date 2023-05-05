from rest_framework import permissions, status
from rest_framework.response import Response
from data_manager.models import Station, StationStatus
from rest_framework.decorators import api_view, permission_classes
from data_manager.models import Station
from data_manager.models import StationStatus
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance 
from django.contrib.gis.db.models.functions import Distance as DistanceFunc
from .serializers import StationPredictorLinearSerializer, StationPredictorMeanSerializer, StationPredictorNearbySerializer
from django.utils import timezone
import itertools, pytz
from .utils.LinearRegression import LinearRegression

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def bikes_predictors_regression(request):
    station_number = request.query_params.get('stationNumber', None)
    if not station_number or not Station.objects.filter(number=station_number).exists():
        return Response({"error": "You have to provide a valid stationNumber"}, status=status.HTTP_400_BAD_REQUEST)
    
    date_param = request.query_params.get('date', None)
    if not date_param:
        return Response({"error": "You have to provide a date"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        parsed_date = timezone.datetime.strptime(date_param, "%Y-%m-%d")
    except ValueError:
        return Response({"error": "The date format is incorrect. It must be in format YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)
    
    #hour param
    hour_param = request.query_params.get('hour', None)
    if not hour_param:
        return Response({"error": "You have to provide an hour"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        parsed_date = timezone.make_aware(timezone.datetime.strptime(date_param+" "+hour_param, "%Y-%m-%d %H:%M:%S"), timezone=pytz.utc)-timezone.timedelta(hours=2)
    except ValueError:
        return Response({"error": "The hour format is incorrect. It must be in format HH:MM:SS"}, status=status.HTTP_400_BAD_REQUEST)
    
    is_future = parsed_date-timezone.make_aware(timezone.datetime.now(), timezone=pytz.utc)

    if is_future != abs(is_future):
        return Response({"error": "You can't predict the past"}, status=status.HTTP_400_BAD_REQUEST)
    
    if is_future > timezone.timedelta(days=7):
        return Response({"error": "You can't predict more than 7 days in the future"}, status=status.HTTP_400_BAD_REQUEST)
    
    station_status_progression = StationStatus.objects.filter(station__number=station_number, last_updated__lte=parsed_date, last_updated__gte=parsed_date-timezone.timedelta(days=30)).order_by('last_updated')
    function_points = [{"x": s.last_updated.timestamp(), "y": s.available_bikes} for s in station_status_progression]
    
    bikes_predicted, regression_function_parameters = _linear_regresion_predictor(parsed_date, station_status_progression)
    
    yourdata= {"prediction": {"x": parsed_date.timestamp(), "y": float(bikes_predicted)}, "evolution": function_points, "linear_function": regression_function_parameters,"station": station_status_progression[0].station}
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
        date = timezone.make_aware(timezone.datetime.strptime(date_param+" "+hour_param, "%Y-%m-%d %H:%M:%S"), timezone=pytz.utc)-timezone.timedelta(hours=2)
    except ValueError:
        return Response({"error": "The hour format is incorrect. It must be in format HH:MM:SS"}, status=status.HTTP_400_BAD_REQUEST)
    
    is_future = date-timezone.make_aware(timezone.datetime.now(), timezone=pytz.utc)

    if is_future != abs(is_future):
        return Response({"error": "You can't predict the past"}, status=status.HTTP_400_BAD_REQUEST)
    
    if is_future > timezone.timedelta(days=7):
        return Response({"error": "You can't predict more than 7 days in the future"}, status=status.HTTP_400_BAD_REQUEST)
    
    mean_prediction = _mean_predictor(station, date.date(), date.time())
    
    station_status_progression = StationStatus.objects.filter(station__number=station_number_param, last_updated__lte=date, last_updated__gte=date-timezone.timedelta(days=30)).order_by('last_updated')
    function_points = [{"x": s.last_updated.timestamp(), "y": s.available_bikes} for s in station_status_progression]

    response_data = {"prediction": [date.timestamp(), mean_prediction], "evolution": function_points, "station": station}
    
    result = StationPredictorMeanSerializer(response_data).data
    return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def station_predictors_nearby(request):
    #latitude param
    latitude_param = request.query_params.get('latitude', None)
    if not latitude_param:
        return Response({"error": "You have to provide a latitude"}, status=status.HTTP_400_BAD_REQUEST)
    try :
        latitude = float(latitude_param)
    except ValueError:
        return Response({"error": "The latitude format is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    
    #longitude param
    longitude_param = request.query_params.get('longitude', None)
    if not longitude_param:
        return Response({"error": "You have to provide a longitude"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        longitude = float(longitude_param)
    except ValueError:
        return Response({"error": "The longitude format is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    
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
        date = timezone.make_aware(timezone.datetime.strptime(date_param+" "+hour_param, "%Y-%m-%d %H:%M:%S"), timezone=pytz.utc)-timezone.timedelta(hours=2)
    except ValueError:
        return Response({"error": "The hour format is incorrect. It must be in format HH:MM:SS"}, status=status.HTTP_400_BAD_REQUEST)
    
    is_future = date-timezone.make_aware(timezone.datetime.now(), timezone=pytz.utc)

    if is_future != abs(is_future):
        return Response({"error": "You can't predict the past"}, status=status.HTTP_400_BAD_REQUEST)
    
    if is_future > timezone.timedelta(days=7):
        return Response({"error": "You can't predict more than 7 days in the future"}, status=status.HTTP_400_BAD_REQUEST)
    
    #minBikes param
    min_bikes_param = request.query_params.get('minBikes', None)
    if not min_bikes_param:
        return Response({"error": "You have to provide a minBikes"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        min_bikes = int(min_bikes_param)
    except ValueError:
        return Response({"error": "The minBikes format is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    if min_bikes < 0:
        return Response({"error": "The minBikes must be positive"}, status=status.HTTP_400_BAD_REQUEST)
    
    #radius param
    radius_param = request.query_params.get('radius', None)
    if not radius_param:
        return Response({"error": "You have to provide a radius"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        radius = float(radius_param)
    except ValueError:
        return Response({"error": "The radius format is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    if radius < 0:
        return Response({"error": "The radius must be positive"}, status=status.HTTP_400_BAD_REQUEST)
    
    #method param
    method_param = request.query_params.get('method', None)
    if not method_param:
        return Response({"error": "You have to provide a method"}, status=status.HTTP_400_BAD_REQUEST)
    method = method_param.lower().strip()
    if method not in ["mean", "linear"]:
        return Response({"error": "The method must be mean or linear"}, status=status.HTTP_400_BAD_REQUEST)
    
    #limit param (optional)
    limit_param = request.query_params.get('limit', None)
    if limit_param:
        try:
            limit = int(limit_param)
        except ValueError:
            return Response({"error": "The limit format is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        if limit <= 0:
            return Response({"error": "The limit must be positive"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        limit = limit_param
        
    response_data = _nearby_predictor(latitude, longitude, date, min_bikes, radius, method, limit)
    result = StationPredictorNearbySerializer(response_data, many=True).data
    return Response(result, status=status.HTTP_200_OK)

# ------------------------------ PRIVATE METHODS ------------------------------ #

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
    
    linear_regressor = LinearRegression(x_points=[x[1] for x in function_points], y_points=[x[0] for x in function_points])
    
    linear_regressor.fit()
    
    linear_regresion_ecuation_coef = linear_regressor.coef
    linear_regresion_ecuation_intercept = linear_regressor.intercept
    
    return (int(linear_regresion_ecuation_coef*(parsed_date.timestamp()-origin_timestamp)+linear_regresion_ecuation_intercept), {
        "coef": linear_regresion_ecuation_coef,
        "intercept": linear_regresion_ecuation_intercept,
    })
    
def _nearby_predictor(latitude, longitude, full_date, min_bikes, radius, method, limit=None):
    result = []
    location = Point(longitude, latitude)
    stations = Station.objects.filter(location__distance_lt=(location, Distance(km=radius))).annotate(distance=DistanceFunc("location", location)).order_by("distance")
    if method == "mean":
        for station in stations:
            prediction = _mean_predictor(station, full_date.date(), full_date.time())
            if prediction >= min_bikes:
                result.append({"prediction": prediction, "station": station}) 
    else:
        for station in stations:
            station_status_progression = StationStatus.objects.filter(station=station, last_updated__lte=full_date, last_updated__gte=full_date-timezone.timedelta(days=30)).order_by('last_updated')
            prediction, _ =_linear_regresion_predictor(full_date, station_status_progression)
            if prediction >= min_bikes:
                result.append({"prediction": prediction, "station": station})
    
    if limit:
        result = result[:limit]
    
    return result