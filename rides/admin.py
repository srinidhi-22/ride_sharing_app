from django.contrib import admin
from .models import Ride, Feedback, SharedRide

admin.site.register(Ride)
admin.site.register(Feedback)
admin.site.register(SharedRide)