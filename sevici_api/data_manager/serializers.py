from django.contrib.auth.models import User
from data_manager.models import Station, StationStatus
from rest_framework import serializers

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class StationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'

class StationStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StationStatus
        fields = ['is_open', 'available_bikes', 'total_capacity', 'last_updated']