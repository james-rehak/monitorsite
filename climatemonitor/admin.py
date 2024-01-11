from django.contrib import admin
from .models import Sensor, Thermostat, SensorType, Setting, UserSetting, Alarm, AlarmEmail

# Register your models here.
admin.site.register([Sensor, SensorType, Thermostat, Setting, UserSetting, Alarm, AlarmEmail])
