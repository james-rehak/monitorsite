from django.db import models
from . import Sensor
from ..utils import * 

class Alarm(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.DO_NOTHING)
    temperature = models.DecimalField(max_digits=5, decimal_places=1) # Celcius
    threshold_mintue = models.DecimalField(max_digits=5, decimal_places=1)
    start_time = models.TimeField()
    end_time = models.TimeField()
    override_sensor = models.ForeignKey(Sensor, on_delete=models.DO_NOTHING, related_name="override_sensors")
    override_temperature = models.DecimalField(max_digits=5, decimal_places=1) # Celcius
    deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.sensor.name} ({self.start_time} - {self.end_time}) {self.temperature}"

    @property
    def temperature_f(self):
        return round(convert_celcius_to_fahrenheit(self.temperature))
    
    @property
    def override_temperature_f(self):
        return round(convert_celcius_to_fahrenheit(self.override_temperature))
    