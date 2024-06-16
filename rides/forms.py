from django import forms
from .models import Ride, Feedback
from django.utils import timezone

class RideForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=timezone.now
    )

    class Meta:
        model = Ride
        fields = ['trip_id', 'driver_name', 'driver_phone', 'cab_number', 'start_time']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comments']

class CompanionDetailsForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Companion's Name")
    phone_number = forms.CharField(max_length=15, required=True, label="Companion's Phone Number")



