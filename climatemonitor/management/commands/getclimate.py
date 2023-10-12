from typing import Any
from django.core.management.base import BaseCommand
from climatemonitor.models import Sensor
from django.utils import timezone



class Command(BaseCommand):
    help = "Request sensor APIs for temperature and humidity data"

    def add_arguments(self, parser):
        parser.add_argument("sensor_type_ids", nargs="+", type=int)

    def handle(self, *args: Any, **options: Any):
        now = timezone.now()
        message = ""
        sensors = Sensor.objects.filter(sensor_type_id__in = options['sensor_type_ids'], deleted = False)

        for sensor in sensors:
            message += sensor.get_reading()

        self.stdout.write(
            self.style.SUCCESS('{} Checked sensors.'.format(now.strftime('%Y-%m-%d %H:%M:%S')))
        )

        if message:
            self.stdout.write(
                self.style.ERROR(message)
            )