from rest_framework import serializers
from data_manager.serializers import StationSerializer

class LinearFunctionSerializer(serializers.Serializer):
   coef = serializers.FloatField()
   intercept = serializers.FloatField()
   
class PointSerializer(serializers.Serializer):
   x = serializers.FloatField()
   y = serializers.FloatField()
   
class StationPredictorLinearSerializer(serializers.Serializer):
   bikes_predicted = serializers.IntegerField()
   evolution = serializers.ListField(child=PointSerializer())
   linear_function = LinearFunctionSerializer()
   station = StationSerializer()

class StationPredictorMeanSerializer(serializers.Serializer):
   prediction = serializers.ListField()
   evolution = serializers.ListField(child=PointSerializer())
   station = StationSerializer()