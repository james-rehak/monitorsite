from django.db import models
from . import Alarm

class AlarmEmail(models.Model):
    alarm = models.ForeignKey(Alarm, on_delete=models.DO_NOTHING)
    email = models.EmailField()
    deleted = models.BooleanField()


    def __str__(self) -> str:
        return f"{self.alarm}: {self.email}"