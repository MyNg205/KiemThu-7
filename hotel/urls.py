from django.urls import path
from . import views

urlpatterns = [
    path('bookings/', views.staff_bookings, name='staff_bookings'),
    path('rooms/', views.staff_rooms, name='staff_rooms'),
]
