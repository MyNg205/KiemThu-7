# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class RoomType(models.Model):
    """Loại phòng (VD: Studio, Deluxe, Twin, Double, ...)"""
    name = models.CharField(max_length=100)  # Studio, Deluxe, Twin, Double, etc.
    description = models.TextField()
    base_price = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField(default=2)
    bed_count = models.PositiveIntegerField(default=1)  # Số giường
    image = models.URLField(blank=True, null=True)
    amenities = models.TextField(default='')  # Tiện nghi: WiFi, TV, AC, etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.base_price:,} VND)"

    class Meta:
        ordering = ['base_price']

class Room(models.Model):
    """Phòng cụ thể trong khách sạn"""
    STATUS_CHOICES = [
        ('available', 'Còn trống'),
        ('occupied', 'Đã thuê'),
        ('maintenance', 'Bảo trì'),
        ('unavailable', 'Không khả dụng'),
    ]

    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20, unique=True)  # 101, 102, 201, etc.
    floor = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"Phòng {self.room_number} - {self.room_type.name}"

    class Meta:
        ordering = ['floor', 'room_number']

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, default='Đã đặt')  # Đã đặt, Đã huỷ, Đã check in
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Phòng {self.room.room_number} ({self.check_in} to {self.check_out})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username
