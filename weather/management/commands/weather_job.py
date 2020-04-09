import requests

from django.core.management.base import BaseCommand
from apscheduler.schedulers.blocking import BlockingScheduler

from weather.models import City
from weather.views import get_city_view


class Command(BaseCommand):

    def handle(self, **options):
        def get_temperatures():
            cities = City.objects.all()
            for c in cities:
                add = get_city_view(requests, city_name=c.city_name)
                print("Get temperature:", c.city_name, add)

        scheduler = BlockingScheduler()
        scheduler.add_job(get_temperatures, 'interval', minutes=1)
        scheduler.start()
