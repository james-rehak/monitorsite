from django.db import models
from . import Sensor
from ..utils import * 
from django.utils import timezone
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To


class Alarm(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.DO_NOTHING)
    temperature = models.DecimalField(max_digits=5, decimal_places=1) # Celcius
    threshold = models.DurationField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    override_sensor = models.ForeignKey(Sensor, on_delete=models.DO_NOTHING, related_name="override_sensors")
    override_temperature = models.DecimalField(max_digits=5, decimal_places=1) # Celcius
    alert_offline = models.BooleanField(default=False)
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
    

    def send_alert(self, offline=False):
        alert = self.alarmhistory_set.create(
            sensor_offline = offline,
            created = timezone.now()
        )

        email_list = {}

        from_email = settings.ALERT_FROM_EMAIL

        if not is_email(from_email):
            print("Done Alerting. No From Email configured.")
            return 

        for alarm_email in self.alarmemail_set.filter(deleted = False):
            email_list[alarm_email.email] = To(alarm_email.email)

        if not email_list:
            print("Done Alerting. No emails associated with Alarm.")
            return 
        
        to_email_list = list(email_list.values())
        email_list_keys = list(email_list.keys())

        subject_text = f"Temperature Alarm: {timezone.localtime(alert.created).strftime('%a, %b %-d, %-I:%M %p')}"

        if offline:
            subject_text = f"Sensor Offline Alarm: {timezone.localtime(alert.created).strftime('%a, %b %-d, %-I:%M %p')}"

        message = Mail(
                from_email= from_email,
                to_emails= to_email_list,
                subject = subject_text,
                html_content=f"Alert for {self} at {timezone.localtime(alert.created).strftime('%Y-%m-%d %H:%M:%S')}"
            )

        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            print(f"Response Status: {response.status_code}")
            print(f"Alerts sent to {email_list_keys}")
        except Exception as e:
            print(e)

        return