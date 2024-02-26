from django.db import models
from . import Alarm

class AlarmHistory(models.Model):
    alarm = models.ForeignKey(Alarm, on_delete=models.DO_NOTHING)
    sensor_offline = models.BooleanField(default=False)
    created = models.DateTimeField("date recorded")

    def __str__(self) -> str:
        offline_text = ""

        if self.sensor_offline:
            offline_text = "Sensor Offline "

        return f"{offline_text}{self.alarm}. Triggered: {self.created: %Y-%m-%d %H:%M:%S}"
    