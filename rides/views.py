# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ride, Feedback, SharedRide
from .forms import RideForm, FeedbackForm, CompanionDetailsForm
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from users.models import CustomUser
from django.contrib import messages
from .utils import send_sms, send_whatsapp
import uuid
# import logging

# logger = logging.getLogger('django')


def initial_home(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'ini_home.html')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def create_ride(request):
    if request.method == 'POST':
        form = RideForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.traveler = request.user
            ride.status = 'in_progress'
            ride.save()
            # Logic to share ride details via WhatsApp or SMS
            return redirect('ride_detail', trip_id=ride.trip_id)
    else:
        form = RideForm(initial={'start_time': timezone.now()})
    return render(request, 'create_ride.html', {'form': form})

@login_required
def ride_detail(request, trip_id):
    ride = get_object_or_404(Ride, trip_id=trip_id)
    if request.user.role == 'Admin' or request.user == ride.traveler or request.user == ride.companion:
        return render(request, 'ride_detail.html', {'ride': ride})
    else:
        return redirect('home')

@login_required
def complete_ride(request, trip_id):
    ride = get_object_or_404(Ride, trip_id=trip_id)
    if request.user == ride.traveler:
        ride.status = 'completed'
        ride.end_time = timezone.now()
        ride.save()

        # Mark the SharedRide as expired
        shared_ride = SharedRide.objects.filter(ride=ride).first()
        if shared_ride:
            shared_ride.expiration_time = timezone.now()
            shared_ride.save()

        # Notify companion about trip completion
        messages.success(request, "Ride completed successfully.")
        return redirect('ride_detail', trip_id=ride.trip_id)
    else:
        messages.error(request, "You are not authorized to complete this ride.")
        return redirect('home')

@login_required
def ride_list(request):
    rides = None
    companionrides = None
    if request.user.role == 'Admin':
        rides = Ride.objects.all()
    elif request.user.role == 'Traveler':
        rides = Ride.objects.filter(traveler=request.user)
    elif request.user.role == 'companion':
        companionrides = Ride.objects.filter(companion=request.user)
    return render(request, 'ride_list.html', {'rides': rides, 'companionrides': companionrides})



@login_required
def share_ride(request, ride_id):
    ride = get_object_or_404(Ride, id=ride_id)
    
    if ride.status != 'in_progress':
        messages.error(request, "Cannot share details for completed trips.")
        return redirect('ride_list')
    
    companion_username = request.POST.get('companion_username')  # Get companion username from form
    
    if request.method == 'POST':
        if companion_username:
            # Search for the companion user based on username
            try:
                companion = CustomUser.objects.get(username=companion_username)
            except CustomUser.DoesNotExist:
                messages.error(request, "Companion not found.")
                return redirect('share_ride', ride_id=ride.id)
            
            # Add the companion to the ride
            ride.companion = companion
            ride.save()
            
            # Logic to send shared link via WhatsApp or SMS
            shared_link = f"http://127.0.0.1:8000/rides/shared/{ride.trip_id}/"  # Replace with actual URL
            expiration_time = timezone.now() + timezone.timedelta(days=1) 
            shared_ride, created = SharedRide.objects.get_or_create(ride=ride, defaults={
                'shared_by': request.user,
                'shared_link': shared_link,
                'expiration_time': expiration_time,
                'companion': companion
            })
            message = f"Ride details: {shared_link}"
            try:
                if request.POST.get('send_via') == 'sms':
                    send_sms(companion.phone_number, message)
                elif request.POST.get('send_via') == 'whatsapp':
                    send_whatsapp(companion.phone_number, message)
                messages.success(request, "Ride details shared successfully.")
            except Exception as e:
                messages.error(request, f"Failed to send message: {str(e)}")
            return redirect('ride_list')
        else:
            messages.error(request, "Companion username is required.")
            return redirect('share_ride', ride_id=ride.id)
    
    return render(request, 'share_ride.html', {'ride': ride})

# views.py
@login_required
def audit_trail(request):
    user = request.user
    shared_rides = Ride.objects.filter(traveler=user)
    return render(request, 'audit_trail.html', {'shared_rides': shared_rides})

@login_required
def give_feedback(request, trip_id):
    ride = get_object_or_404(Ride, trip_id=trip_id)
    if request.user.role == 'companion':
        if request.method == 'POST':
            form = FeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.save(commit=False)
                feedback.ride = ride
                feedback.companion = request.user
                feedback.save()
                return redirect('ride_detail', trip_id=ride.trip_id)
        else:
            form = FeedbackForm()
        return render(request, 'give_feedback.html', {'form': form, 'ride': ride})
    else:
        return redirect('home')
    
    
@login_required
def admin_dashboard(request):
    if request.user.role == 'Admin':
        feedbacks = Feedback.objects.all()
        return render(request, 'admin_dashboard.html', {'feedbacks': feedbacks})
    else:
        return redirect('home')