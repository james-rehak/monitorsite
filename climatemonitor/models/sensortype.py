from django.db import models

# Create your models here.
class SensorType(models.Model):
    name = models.CharField(max_length=255)
    internal_name = models.CharField(max_length=255)
    deleted = models.BooleanField(default=False)


    def __str__(self) -> str:
        return f"{self.id}: {self.name}"
    