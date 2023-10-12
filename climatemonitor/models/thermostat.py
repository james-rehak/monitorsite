from django.db import models
import requests
import json
import datetime
from django.utils import timezone
from ..utils import * 
from . import Sensor
from django.conf import settings
from colorfield.fields import ColorField


class Thermostat(models.Model):
    name = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255)
    set_color = ColorField(default='#696969')
    state_color = ColorField(default='#FFA500')
    deleted = models.BooleanField(default=False)
    

    def __str__(self) -> str:
        return self.name
    
    def record_status(self):
        message = ""
        sensor = Sensor.objects.get(device_identifier = self.identifier)

        headers = {'Authorization': 'Bearer: ' + settings.SMARTTHINGS_API_KEY}
        url = "https://api.smartthings.com/v1/devices/{}/status".format(self.identifier)
        response = requests.get(url, headers=headers)

        try:
            data = json.loads(response.content)
            temperature = data.get('components').get('main').get('temperatureMeasurement').get('temperature').get('value')
            temperature_unit = data.get('components').get('main').get('temperatureMeasurement').get('temperature').get('unit')
            humidity = data.get('components').get('main').get('relativeHumidityMeasurement').get('humidity').get('value')
            operating_state = data.get('components').get('main').get('thermostatOperatingState').get('thermostatOperatingState').get('value')
            set_temperature = data.get('components').get('main').get('thermostatHeatingSetpoint').get('heatingSetpoint').get('value')
            mode = data.get('components').get('main').get('thermostatMode').get('thermostatMode').get('value')


            if temperature_unit.upper() == "F":
                set_temperature = convert_fahrenheit_to_celsius(set_temperature)
                temperature = convert_fahrenheit_to_celsius(temperature)

            now = timezone.now()
            self.thermostathistory_set.create(
                operating_state = operating_state,
                set_temperature = set_temperature,
                mode = mode,
                created = now
            )

            if sensor:
                sensor.reading_set.create(
                    temperature = temperature,
                    humidity = humidity,
                    created = now
                )

        except Exception as e:
            message = "Error: Updating {} status \n".format(self.name)
            print(response.status_code)
            print(e)

        return message

