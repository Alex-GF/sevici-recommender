from django.core.management.base import BaseCommand
from django.conf import settings
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

        print(data[0])

