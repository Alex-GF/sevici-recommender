from data_manager.models import Station, StationStatus
from rest_framework import serializers

# Serializers define the API representation.
class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'

class StationStatusSerializer(serializers.ModelSerializer):
    station = StationSerializer
    class Meta:
        model = StationStatus
        fields = '__all__'
        depth = 1
        