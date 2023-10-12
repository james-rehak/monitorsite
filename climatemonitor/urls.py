from django.urls import path
from . import views

app_name = "climatemonitor"

urlpatterns = [
    path("", views.index, name = 'index'),
]
