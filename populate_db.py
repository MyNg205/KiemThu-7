<<<<<<< HEAD
from _script_setup import setup

setup()

from hotel.models import Room, RoomType


ROOM_TYPES = [
    {
        "name": "Studio",
        "description": "Modern room for two guests.",
        "base_price": 1200000,
        "capacity": 2,
        "bed_count": 1,
        "amenities": "WiFi, TV, AC, Minibar",
        "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=600&q=80",
    },
    {
        "name": "Deluxe",
        "description": "Large room with upgraded amenities.",
        "base_price": 1600000,
        "capacity": 3,
        "bed_count": 1,
        "amenities": "WiFi, TV, AC, Minibar, Balcony",
        "image": "https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=600&q=80",
    },
    {
        "name": "Family",
        "description": "Family room with extra sleeping space.",
        "base_price": 2000000,
        "capacity": 4,
        "bed_count": 2,
        "amenities": "WiFi, TV, AC, Minibar, Kitchen",
        "image": "https://images.unsplash.com/photo-1507089947368-19c1da9775ae?auto=format&fit=crop&w=600&q=80",
    },
    {
        "name": "Suite",
        "description": "Premium suite with a separate lounge area.",
        "base_price": 2500000,
        "capacity": 2,
        "bed_count": 1,
        "amenities": "WiFi, TV, AC, Minibar, Jacuzzi",
        "image": "https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?auto=format&fit=crop&w=600&q=80",
    },
]

ROOMS = [
    {"room_number": "101", "floor": 1, "room_type_name": "Studio"},
    {"room_number": "102", "floor": 1, "room_type_name": "Studio"},
    {"room_number": "103", "floor": 1, "room_type_name": "Studio"},
    {"room_number": "202", "floor": 2, "room_type_name": "Deluxe"},
    {"room_number": "301", "floor": 3, "room_type_name": "Family"},
    {"room_number": "302", "floor": 3, "room_type_name": "Family"},
    {"room_number": "303", "floor": 3, "room_type_name": "Family"},
    {"room_number": "401", "floor": 4, "room_type_name": "Suite"},
    {"room_number": "402", "floor": 4, "room_type_name": "Suite"},
    {"room_number": "403", "floor": 4, "room_type_name": "Suite"},
]


def seed_room_types():
    for data in ROOM_TYPES:
        room_type, created = RoomType.objects.update_or_create(
            name=data["name"],
            defaults=data,
        )
        action = "Created" if created else "Updated"
        print(f"{action} room type: {room_type.name}")


def seed_rooms():
    expected_numbers = {room["room_number"] for room in ROOMS}
    Room.objects.exclude(room_number__in=expected_numbers).delete()

    for data in ROOMS:
        room_type = RoomType.objects.get(name=data["room_type_name"])
        room, created = Room.objects.update_or_create(
            room_number=data["room_number"],
            defaults={
                "room_type": room_type,
                "floor": data["floor"],
                "status": "available",
            },
        )
        action = "Created" if created else "Updated"
        print(f"{action} room: {room.room_number}")


if __name__ == "__main__":
    seed_room_types()
    seed_rooms()
    print(f"\nTotal room types: {RoomType.objects.count()}")
    print(f"Total rooms: {Room.objects.count()}")
=======
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KIEMTHU.settings')
import django
django.setup()
from hotel.models import RoomType, Room

# Create RoomTypes
room_types_data = [
    {
        'name': 'Studio',
        'description': 'Phòng Studio hiện đại, nội thất gỗ, view thành phố, phù hợp cho 2 người lớn.',
        'base_price': 1200000,
        'capacity': 2,
        'bed_count': 1,
        'amenities': 'WiFi, TV, AC, Minibar',
        'image': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=600&q=80',
    },
    {
        'name': 'Deluxe',
        'description': 'Phòng Deluxe rộng rãi, giường đôi lớn, view biển, tiện nghi cao cấp.',
        'base_price': 1600000,
        'capacity': 3,
        'bed_count': 1,
        'amenities': 'WiFi, TV, AC, Minibar, Balcony',
        'image': 'https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=600&q=80',
    },
    {
        'name': 'Family',
        'description': 'Phòng Family cho gia đình, 2 giường đôi, không gian rộng, phù hợp 4 người.',
        'base_price': 2000000,
        'capacity': 4,
        'bed_count': 2,
        'amenities': 'WiFi, TV, AC, Minibar, Kitchen',
        'image': 'https://images.unsplash.com/photo-1507089947368-19c1da9775ae?auto=format&fit=crop&w=600&q=80',
    },
    {
        'name': 'Suite',
        'description': 'Suite cao cấp, phòng khách riêng, bồn tắm, view toàn cảnh thành phố.',
        'base_price': 2500000,
        'capacity': 2,
        'bed_count': 1,
        'amenities': 'WiFi, TV, AC, Minibar, Jacuzzi',
        'image': 'https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?auto=format&fit=crop&w=600&q=80',
    },
]

for data in room_types_data:
    rt, created = RoomType.objects.get_or_create(name=data['name'], defaults=data)
    if created:
        print(f"Created RoomType: {rt}")
    else:
        # Update existing
        for key, value in data.items():
            setattr(rt, key, value)
        rt.save()
        print(f"Updated RoomType: {rt}")

# Create Rooms
rooms_data = [
    {'room_number': '101', 'floor': 1, 'room_type_name': 'Studio'},
    {'room_number': '102', 'floor': 1, 'room_type_name': 'Studio'},
    {'room_number': '103', 'floor': 1, 'room_type_name': 'Studio'},
    {'room_number': '202', 'floor': 2, 'room_type_name': 'Deluxe'},
    {'room_number': '301', 'floor': 3, 'room_type_name': 'Family'},
    {'room_number': '401', 'floor': 4, 'room_type_name': 'Suite'},
    {'room_number': '302', 'floor': 3, 'room_type_name': 'Family'},
    {'room_number': '303', 'floor': 3, 'room_type_name': 'Family'},
    {'room_number': '402', 'floor': 4, 'room_type_name': 'Suite'},
    {'room_number': '403', 'floor': 4, 'room_type_name': 'Suite'},
]


# First, delete existing rooms not in the list
existing_rooms = Room.objects.all()
for room in existing_rooms:
    if room.room_number not in [data['room_number'] for data in rooms_data]:
        room.delete()
        print(f"Deleted Room: {room}")
for data in rooms_data:
    rt = RoomType.objects.get(name=data['room_type_name'])
    room, created = Room.objects.get_or_create(room_number=data['room_number'], defaults={'room_type': rt, 'floor': data['floor']})
    if created:
        print(f"Created Room: {room}")
    else:
        print(f"Room already exists: {room}")

print(f"\nTotal RoomTypes: {RoomType.objects.count()}")
print(f"Total Rooms: {Room.objects.count()}")
>>>>>>> be15ac174ec3f04303fa614df98f2bb4f6e9f869
