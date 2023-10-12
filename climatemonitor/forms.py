from django import forms
from django.utils import timezone
import datetime
from django.core.exceptions import ValidationError

class DateTimeLocalInput(forms.DateTimeInput):
    input_type = "datetime-local"
 
class DateTimeLocalField(forms.DateTimeField):
    input_formats = [
        "%Y-%m-%dT%H:%M:%S", 
        "%Y-%m-%dT%H:%M:%S.%f", 
        "%Y-%m-%dT%H:%M"
    ]
    widget = DateTimeLocalInput(format="%Y-%m-%dT%H:%M")



class SearchForm(forms.Form):
    units = (
        ('c', 'C'),
        ('f', 'F')
    )
    unit = forms.ChoiceField(label="Unit",choices=units, initial='c')
    
    start_date = DateTimeLocalField(
        label= "Start Time",
        initial= timezone.now()- datetime.timedelta(hours=6),
        required= True
    )

    end_date = DateTimeLocalField(
        label= "End Time",
        initial= timezone.now(),
        required= True
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date > end_date:
            raise ValidationError("Start Date cannot be later than End Date")