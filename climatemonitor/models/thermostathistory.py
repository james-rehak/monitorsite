from django.db import models
from . import Thermostat
from ..utils import * 


class ThermostatHistory(models.Model):
    thermostat = models.ForeignKey(Thermostat, on_delete=models.DO_NOTHING)
    operating_state = models.CharField(max_length=100) # Idle or Heat
    set_temperature = models.DecimalField(max_digits=5, decimal_places=1)
    temperature = models.DecimalField(max_digits=5, decimal_places=1)
    mode = models.CharField(max_length=100)
    created = models.DateTimeField("date recorded")

    def __str__(self):
        return self.thermostat + ' ' + self.operating_state + ' ' + self.set_temperature
    
    @property
    def set_temperature_f(self):
        return round(convert_celcius_to_fahrenheit(self.set_temperature))
    
    @property
    def temperature_f(self):
        return round(convert_celcius_to_fahrenheit(self.temperature))
    