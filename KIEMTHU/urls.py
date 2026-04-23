"""
URL configuration for KIEMTHU project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from hotel import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
<<<<<<< HEAD
    path('register/', views.register_view, name='register'),
=======
>>>>>>> be15ac174ec3f04303fa614df98f2bb4f6e9f869
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('booking-history/', views.booking_history, name='booking_history'),
    path('book-room/', views.select_room_to_book, name='select_room_to_book'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    path('room-type/<int:room_type_id>/', views.room_type_detail, name='room_type_detail'),
    path('book/<int:room_id>/', views.book_room, name='book_room_with_id'),
    path('book/', views.book_room, name='book_room'),
    path('staff/', views.staff_home, name='staff_home'),
    path('staff/', include('hotel.urls')),
]
