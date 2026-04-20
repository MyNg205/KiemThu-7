#!/usr/bin/env python
"""Script để thêm phòng mới cho mỗi loại phòng"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KIEMTHU.settings')
django.setup()

from hotel.models import RoomType, Room
import random

print("Đang thêm phòng mới...")

for room_type in RoomType.objects.all():
    existing_count = room_type.rooms.count()
    print(f"\n{room_type.name}:")
    print(f"  - Phòng hiện tại: {existing_count}")
    
    # Thêm 5 phòng mới cho mỗi loại
    for i in range(existing_count + 1, existing_count + 6):
        room_number = f"{room_type.name[:2].upper()}{i:03d}"
        floor = random.randint(1, 5)
        
        room, created = Room.objects.get_or_create(
            room_type=room_type,
            room_number=room_number,
            defaults={'floor': floor, 'status': 'available'}
        )
        
        if created:
            print(f"  ✓ Thêm phòng {room_number} (Tầng {floor})")
        else:
            print(f"  - Phòng {room_number} đã tồn tại")
    
    new_count = room_type.rooms.count()
    print(f"  → Tổng cộng: {new_count} phòng")

print("\n✅ Hoàn tất!")

