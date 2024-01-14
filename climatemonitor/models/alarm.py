from django.db import models
from . import Sensor
from ..utils import * 
from django.utils import timezone


class Alarm(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.DO_NOTHING)
    temperature = models.DecimalField(max_digits=5, decimal_places=1) # Celcius
    threshold = models.DurationField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    override_sensor = models.ForeignKey(Sensor, on_delete=models.DO_NOTHING, related_name="override_sensors")
    override_temperature = models.DecimalField(max_digits=5, decimal_places=1) # Celcius
    deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.sensor.name} ({self.start_time} - {self.end_time}): {self.temperature}"
    
    def display_range(self):
        return f"{self.start_time} - {self.end_time}"

    @property
    def temperature_f(self):
        return round(convert_celcius_to_fahrenheit(self.temperature))
    
    @property
    def override_temperature_f(self):
        return round(convert_celcius_to_fahrenheit(self.override_temperature))
    

    def send_alert(self):
        self.alarmhistory_set.create(
            created = timezone.now()
        )
        for alarm_email in self.alarmemail_set.filter(deleted = False):
            alarm_email.send_mail()