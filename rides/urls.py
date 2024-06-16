from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('create/', views.create_ride, name='create_ride'),
    path('<str:trip_id>/', views.ride_detail, name='ride_detail'),
    path('<str:trip_id>/complete/', views.complete_ride, name='complete_ride'),
    path('<str:trip_id>/feedback/', views.give_feedback, name='give_feedback'),
    path('all_rides', views.ride_list, name='ride_list'),
    path('share_ride/<int:ride_id>/', views.share_ride, name='share_ride'),
]
