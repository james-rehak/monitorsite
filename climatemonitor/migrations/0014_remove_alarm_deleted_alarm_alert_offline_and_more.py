# Generated by Django 4.2.6 on 2024-02-25 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('climatemonitor', '0013_rename_threshold_mintue_alarm_threshold'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarm',
            name='alert_offline',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='alarmhistory',
            name='sensor_offline',
            field=models.BooleanField(default=False),
        ),
    ]
