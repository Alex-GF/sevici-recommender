from rest_framework import views
from rest_framework.response import Response

from data_manager.models import Station

from .serializers import StationPredictorSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def bikes_predictors(request):
    yourdata= {"bikes_predicted": 7, "station": Station.objects.all()[0]}
    results = StationPredictorSerializer(yourdata).data
    return Response(results, status=status.HTTP_200_OK)

def _mean_predictor():
    pass

def _linear_regresion_predictor():
    pass