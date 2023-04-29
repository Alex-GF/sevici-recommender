from django.contrib.auth.models import User
from data_manager.models import Station
from rest_framework import serializers

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class StationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Station
#        fields = ['number', 'address', 'status', 'is_open', 'available_bikes', 'total_capacity', 'location', 'last_updated']