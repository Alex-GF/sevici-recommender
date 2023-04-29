from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

class Station(models.Model):
    number = models.PositiveIntegerField(primary_key=True, unique=True)
    address = models.CharField(max_length=200)
    location = models.PointField(geography=True, default=Point(0.0, 0.0), unique=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    available_bikes = models.IntegerField(default=0)
    total_capacity = models.IntegerField(default=0)
    is_open = models.BooleanField(default=True)

    @property
    def longitude(self):
        return self.location.x
    
    @property
    def latitude(self):
        return self.location.y