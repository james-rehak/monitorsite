from django.db import models
from . import Sensor
from ..utils import * 


class Reading(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    temperature = models.DecimalField(max_digits=5, decimal_places=1) # always Celcius
    humidity = models.DecimalField(max_digits=5, decimal_places=1)
    created = models.DateTimeField("date recorded")

    def __str__(self):
        # return str(self.sensor) + ' ' + str(self.temperature) + ' ' + str(self.created.strftime('%Y-%m-%d %H:%M:%S'))
        return "{} {} {}".format(self.sensor, self.temperature, self.created.strftime('%Y-%m-%d %H:%M:%S'))
    
    @property
    def temperature_f(self):
        return round(convert_celcius_to_fahrenheit(self.temperature))
