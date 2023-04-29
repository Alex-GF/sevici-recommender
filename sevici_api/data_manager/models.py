from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

class Station(models.Model):
    number = models.PositiveIntegerField(primary_key=True, unique=True)
    address = models.CharField(max_length=200)
    location = models.PointField(geography=True, default=Point(0.0, 0.0), unique=True)

    @property
    def longitude(self):
        return self.location.x
    
    @property
    def latitude(self):
        return self.location.y
    
class StationStatus(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    is_open = models.BooleanField(default=True)
    available_bikes = models.IntegerField(default=0)
    total_capacity = models.IntegerField(default=0)
    last_updated = models.DateTimeField()