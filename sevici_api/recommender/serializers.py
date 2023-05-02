from rest_framework import serializers
from data_manager.serializers import StationSerializer

class StationPredictorSerializer(serializers.Serializer):
   """Your data serializer, define your fields here."""
   bikes_predicted = serializers.IntegerField()
   station = StationSerializer()