<<<<<<< HEAD
from populate_db import seed_room_types, seed_rooms


if __name__ == "__main__":
    seed_room_types()
    seed_rooms()
=======
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KIEMTHU.settings')
django.setup()

from hotel.models import Room

# Xóa phòng cũ
Room.objects.all().delete()

# Tạo dữ liệu mẫu
rooms_data = [
    {
        'name': 'Studio Room',
        'room_type': 'Studio',
        'price': 1200000,
        'description': 'Phòng Studio hiện đại, nội thất gỗ, view thành phố, phù hợp cho 2 người lớn.',
        'capacity': 2,
        'image': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=600&q=80',
    },
    {
        'name': 'Deluxe Room',
        'room_type': 'Deluxe',
        'price': 1600000,
        'description': 'Phòng Deluxe rộng rãi, giường đôi lớn, view biển, tiện nghi cao cấp.',
        'capacity': 3,
        'image': 'https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=600&q=80',
    },
    {
        'name': 'Family Room',
        'room_type': 'Family',
        'price': 2000000,
        'description': 'Phòng Family cho gia đình, 2 giường đôi, không gian rộng, phù hợp 4 người.',
        'capacity': 4,
        'image': 'https://images.unsplash.com/photo-1507089947368-19c1da9775ae?auto=format&fit=crop&w=600&q=80',
    },
    {
        'name': 'Luxury Suite',
        'room_type': 'Luxury',
        'price': 2500000,
        'description': 'Suite cao cấp, phòng khách riêng, bồn tắm, view toàn cảnh thành phố.',
        'capacity': 2,
        'image': 'https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?auto=format&fit=crop&w=600&q=80',
    },
    {
        'name': 'Apartment',
        'room_type': 'Apartment',
        'price': 1800000,
        'description': 'Căn hộ mini, bếp riêng, phù hợp cho nhóm bạn hoặc gia đình nhỏ.',
        'capacity': 3,
        'image': 'https://images.unsplash.com/photo-1505691938895-1758d7feb511?auto=format&fit=crop&w=600&q=80',
    },
    {
        'name': 'Suite Ocean View',
        'room_type': 'Suite',
        'price': 3000000,
        'description': 'Suite hướng biển, ban công riêng, nội thất sang trọng, miễn phí minibar.',
        'capacity': 2,
        'image': 'https://images.unsplash.com/photo-1503676382389-4809596d5290?auto=format&fit=crop&w=600&q=80',
    },
]

for data in rooms_data:
    Room.objects.create(**data)
    print(f"✅ Created room: {data['name']}")

print(f"\n✅ Total rooms created: {Room.objects.count()}")


>>>>>>> be15ac174ec3f04303fa614df98f2bb4f6e9f869
