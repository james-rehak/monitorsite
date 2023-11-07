from django.db import models
from . import SensorType
import requests
import json
from django.utils import timezone
from ..utils import * 
import datetime
from django.conf import settings
from colorfield.fields import ColorField



class Sensor(models.Model):
    sensor_type = models.ForeignKey(SensorType, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    color = ColorField(default='#696969')
    device_identifier = models.CharField(max_length=255) # IP address or deviceId
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def get_reading(self):
        from . import Thermostat
        message = ""
        now = timezone.now()
        match self.sensor_type.internal_name:
            case "dht22":
                url = "http://{}/readings".format(self.device_identifier)

                try:
                    response = requests.get(url)
                    data = json.loads(response.content)

                    if data.get('response') != "success":
                        raise Exception("Bad JSON response")
                    
                    self.reading_set.create(
                        temperature = data.get('temperature'), 
                        humidity = data.get('humidity'), 
                        created = now
                    )                    
                except Exception as e:
                    message = "{} Error: {} sensor climate data not recorded \n".format(now.strftime('%Y-%m-%d %H:%M:%S'), self.name)
                    print(e)

            case "smartthings_thermostat":
                thermostat = Thermostat.objects.get(identifier = self.device_identifier)

                headers = {'Authorization': 'Bearer: ' + settings.SMARTTHINGS_API_KEY}
                url = "https://api.smartthings.com/v1/devices/{}/status".format(self.device_identifier)
                try:
                    response = requests.get(url, headers=headers)
                    data = json.loads(response.content)
                    temperature = data.get('components').get('main').get('temperatureMeasurement').get('temperature').get('value')
                    temperature_unit = data.get('components').get('main').get('temperatureMeasurement').get('temperature').get('unit')
                    humidity = data.get('components').get('main').get('relativeHumidityMeasurement').get('humidity').get('value')
                    operating_state = data.get('components').get('main').get('thermostatOperatingState').get('thermostatOperatingState').get('value')
                    set_temperature = data.get('components').get('main').get('thermostatHeatingSetpoint').get('heatingSetpoint').get('value')
                    mode = data.get('components').get('main').get('thermostatMode').get('thermostatMode').get('value')

                    # operating_timestamp = data.get('components').get('main').get('thermostatOperatingState').get('thermostatOperatingState').get('timestamp')
                    # operating_time = datetime.datetime.fromisoformat(operating_timestamp)
                    
                    # Save all temps as C in db
                    if temperature_unit.upper() == "F":
                        temperature = convert_fahrenheit_to_celsius(temperature)
                        set_temperature = convert_fahrenheit_to_celsius(set_temperature)

                    self.reading_set.create(
                        temperature = temperature, 
                        humidity = humidity, 
                        created = now
                    )

                    if thermostat:
                        thermostat.thermostathistory_set.create(
                            operating_state = operating_state,
                            set_temperature = set_temperature,
                            temperature = temperature,
                            mode = mode,
                            created = now
                        )
                    
                except Exception as e:
                    message = "{} Error: {} sensor climate data not recorded \n".format(now.strftime('%Y-%m-%d %H:%M:%S'), self.name)
                    print(e)
            case "noaa":
                url = "https://api.weather.gov/gridpoints/{}/forecast/hourly".format(self.device_identifier) # LWX/109,91

                try:
                    response = requests.get(url)
                    data = json.loads(response.content)
                    periods = data.get('properties').get('periods')

                    for period in periods:
                        start_time = datetime.datetime.fromisoformat(period.get('startTime')) # timezone aware
                        end_time = datetime.datetime.fromisoformat(period.get('endTime'))
                        temperature_unit = period.get('temperatureUnit')
                        temperature = period.get('temperature')
                        humidity = period.get('relativeHumidity').get('value')

                        if temperature_unit.upper() == "F":
                            temperature = convert_fahrenheit_to_celsius(temperature)

                        if start_time < now and end_time >= now:
                            self.reading_set.create(
                                temperature = temperature, 
                                humidity = humidity, 
                                created = now
                            )
                            break
                    
                except Exception as e:
                    message = "{} Error: {} sensor climate data not recorded \n".format(now.strftime('%Y-%m-%d %H:%M:%S'), self.name)
                    print(e)                

            case _:
                message = "{} Error: No sensor Type Found \n".format(now.strftime('%Y-%m-%d %H:%M:%S'))
            
        return message
    