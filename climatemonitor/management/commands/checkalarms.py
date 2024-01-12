from typing import Any
from django.core.management.base import BaseCommand
from climatemonitor.models import Alarm, Reading
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = "Check if any of the alarm are triggered"

    def handle(self, *args: Any, **options: Any) -> str | None:
        now = timezone.now()
        local_time = timezone.localtime().time()
        alarms = Alarm.objects.filter(deleted = False)

        for alarm in alarms:
            print(alarm)

            if alarm.start_time <= local_time <= alarm.end_time:
                print(f"{local_time} is inbetween {alarm.start_time} and {alarm.end_time}")

                threshold_time = now - alarm.threshold
                print(f"{now} - {threshold_time}")

                sensor = alarm.sensor

                current_temperature = sensor.reading_set.filter(created__gte = threshold_time).values_list("temperature", flat=True).last()
                # last_reading = sensor.reading_set.filter(created__gte = threshold_time).last()
                print(current_temperature)

                if current_temperature and current_temperature < alarm.temperature:
                    print("trigger the alarms")
                    alert_sent = alarm.alarmhistory_set.filter(created__gte = threshold_time).last()

                    if not alert_sent:
                        alarm.send_alert()
                    else:
                        print(f"Alert already sent on {alert_sent.created}")
                        
                else:
                    print(f"current_temp: {current_temperature}, alarm temp: {alarm.temperature}")

            else:
                print(f"{local_time} is NOT inbetween {alarm.start_time} and {alarm.end_time}")
                