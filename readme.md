# Monitor Site
![Workflow](https://github.com/james-rehak/monitorsite/actions/workflows/django.yml/badge.svg)

Is a IoT web application that polls temperature sensors and services to store and display temperature and thermostat data in a building with a central heating system. This data can be used for a variety of purposes, such as:
- Energy management: Temperature data can be used to track energy consumption and identify areas where energy savings can be achieved.
- HVAC control: Temperature data can be used to control heating, ventilation, and air conditioning (HVAC) systems to maintain a comfortable and efficient temperature environment.
- Environmental monitoring: Temperature data can be used to monitor environmental conditions and identify potential problems, such as equipment failure or hazardous conditions.

Monitor Site is currently capable of polling RaspberryPis with DHT22 Sensors Running [Sensor Server](https://github.com/james-rehak/sensor), Samsung's [Smartthings API](https://developer.smartthings.com/docs/api/public/) for Thermostat Data, and the National Oceanic and Atmospheric Administration's (NOAA) [API Web Service](https://www.weather.gov/documentation/services-web-api) for external temperatures from the closest weather station.

## Configuration
- Create config.json based on example-config.json in project directory
- Deploy with Gunicorn and ngnix
- Add cron jobs to poll sensors:
```
*/5 * * * * cd project_dir && project_dir/env/bin/python project_dir/manage.py getclimate {sensor_type_ids} >> project_dirlogs/get_internal_temps 2>&1
```


## Roadmap
- Add Users Accounts for preferences
- Add Alerts with email notifications
- Async Frontend
- Deploy as Progressive Web App
- Automated and predictive Thermostat Control based on internal and external input data
