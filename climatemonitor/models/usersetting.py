from django.db import models
from django.contrib.auth.models import User
from . import Setting

class UserSetting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    class Meta:
        models.UniqueConstraint(fields=['user', 'setting'], name="user_setting")

    
    def __str__(self):
        return f"{self.user.username}-{self.setting.name}: {self.value}"
        

