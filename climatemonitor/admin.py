from django.contrib import admin
from .models import Sensor, Thermostat, SensorType

# Register your models here.
admin.site.register([Sensor, SensorType, Thermostat])
