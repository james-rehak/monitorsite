from django.shortcuts import HttpResponse, render, redirect
from django.template import loader
from .models import Sensor, Thermostat, UserSetting
from django.utils import timezone
import datetime
from django.template.defaulttags import register
from .forms import SearchForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages



@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@login_required
def index(request):
    template = loader.get_template("climatemonitor/index.html")
    sensor_readings = {}
    sensor_humidity = {}
    thermostat_history = {}
    user = request.user
    
    sensors = Sensor.objects.filter(deleted = False)
    thermostats = Thermostat.objects.filter(deleted = False)

    display_unit = {'c': 'C', 'f': 'F'}

    prefered_unit = user.usersetting_set.filter(setting__name="temperature unit").first()

    if prefered_unit:
        prefered_unit = prefered_unit.value.lower()

    if prefered_unit not in ['c','f']:
        prefered_unit = 'c'


    form = SearchForm(initial={
        'unit': prefered_unit, 
        'start_date': timezone.now()- datetime.timedelta(hours=2),
        'end_date': timezone.now()
    })
    
    unit = form.initial.get('unit')
    start_date = form.initial.get('start_date')
    end_date = form.initial.get('end_date')


    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            unit = form.cleaned_data.get('unit')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')


    for sensor in sensors:
        sensor_readings[sensor] = sensor.reading_set.filter(created__gte = start_date, created__lte = end_date)

        for reading in sensor_readings[sensor]:
            print(reading)


    for thermostat in thermostats:
        thermostat_history[thermostat] = thermostat.thermostathistory_set.filter(created__gte = start_date, created__lte = end_date)


    context = {
        "sensors": sensors,
        "sensor_readings": sensor_readings,
        "thermostat_history" : thermostat_history,
        "form": form,
        "unit": unit,
        "display_unit": display_unit
    }

    return HttpResponse(template.render(context, request))


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('climatemonitor:index')
        else:
            messages.success(request, ("Invalid Login!"))
            return redirect('climatemonitor:signin')
        
    return render(request, 'climatemonitor/auth/login.html')

def signout(request):
    logout(request)
    messages.success(request, ("Successfully Logged Out!"))
    return redirect('climatemonitor:signin')