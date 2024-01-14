from django.db import models
from . import Alarm

class AlarmHistory(models.Model):
    alarm = models.ForeignKey(Alarm, on_delete=models.DO_NOTHING)
    created = models.DateTimeField("date recorded")

    def __str__(self) -> str:
        return f"{self.alarm}. Triggered: {self.created: %Y-%m-%d %H:%M:%S}"