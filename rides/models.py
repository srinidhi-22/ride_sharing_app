from django.db import models

# Create your models here.from django.db import models
from users.models import CustomUser
from django.utils import timezone
from django.conf import settings

class Ride(models.Model):
    trip_id = models.CharField(max_length=100, unique=True)
    driver_name = models.CharField(max_length=100)
    driver_phone = models.CharField(max_length=15)
    cab_number = models.CharField(max_length=20)
    traveler = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='traveler_rides')
    companion = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='companion_rides')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    audit_trail = models.TextField(blank=True)  # Log of ride sharing
    status = models.CharField(max_length=20)  # e.g., 'in_progress', 'completed'
    cab_location = models.CharField(max_length=100, blank=True)  # Added field for cab location

    def __str__(self):
        return f"Ride {self.trip_id} - {self.driver_name}"

class Feedback(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='feedbacks')
    companion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField()

    def __str__(self):
        return f"Feedback for Ride {self.ride.trip_id} by {self.companion.username}"

class SharedRide(models.Model):
    ride = models.OneToOneField(Ride, on_delete=models.CASCADE)
    shared_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    shared_link = models.CharField(max_length=100, unique=True)
    expiration_time = models.DateTimeField()
    companion = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='shared_companion')

    def is_expired(self):
        return timezone.now() > self.expiration_time or self.ride.status == 'completed'

    def __str__(self):
        return f"Shared Ride {self.ride.trip_id} by {self.shared_by.username}"
