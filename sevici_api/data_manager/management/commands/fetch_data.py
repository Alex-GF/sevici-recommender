from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.gis.geos import Point
from data_manager.models import Station, StationStatus
import os, requests

class Command(BaseCommand):
        
    help = 'Fetch data from SEVICI'

    def handle(self, *args, **options):
        
        URL = "https://api.jcdecaux.com/vls/v3/stations"

        api_key = settings.API_KEY
        contract = settings.CONTRACT

        print(api_key)

        PARAMS = {'apiKey':api_key, 'contract':contract}

        r = requests.get(url = URL, params = PARAMS)

        data = r.json()
        stations_status = []
        
        for station in data:

            number = station['number']
            address = station['address']
            is_open = station['status'] == 'OPEN'
            available_bikes = station['totalStands']['availabilities']['bikes']
            total_capacity = station['totalStands']['capacity']
            location = Point(x=station['position']['longitude'], y=station['position']['latitude'])
            last_updated = station['lastUpdate']

            station, _ = Station.objects.get_or_create(number=number, address=address, location=location)
            station_status = StationStatus(station=station, is_open=is_open, available_bikes=available_bikes, total_capacity=total_capacity, last_updated=last_updated)

            stations_status.append(station_status)

        StationStatus.objects.bulk_create(stations_status)

