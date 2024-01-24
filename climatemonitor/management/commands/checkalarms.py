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

        self.stdout.write(
            self.style.SUCCESS(f"Checking Alarms {now.strftime('%Y-%m-%d %H:%M:%S')}")
        )

        for alarm in alarms:
            message = ""
            if alarm.start_time <= local_time <= alarm.end_time:
                self.stdout.write(
                    self.style.HTTP_INFO(f"{alarm} at {local_time} is inbetween {alarm.start_time} and {alarm.end_time}")
                )
                threshold_time = now - alarm.threshold

                sensor = alarm.sensor

                current_temperature = sensor.reading_set.filter(created__gte = threshold_time).values_list("temperature", flat=True).last()

                if current_temperature and current_temperature < alarm.temperature:
                    alert_sent = alarm.alarmhistory_set.filter(created__gte = threshold_time).last()

                    if not alert_sent:
                        alarm.send_alert()
                    else:
                        message += f"Alert already sent on {alert_sent.created}\n"
                else:
                    message += f"current_temp: {current_temperature}, alarm temp: {alarm.temperature}\n"
            else:
                message += f"{alarm} at {local_time} is NOT inbetween {alarm.start_time} and {alarm.end_time}\n"
            
            self.stdout.write(
                self.style.HTTP_INFO(message)
            )


                