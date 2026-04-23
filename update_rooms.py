<<<<<<< HEAD
from _script_setup import setup

setup()

from hotel.models import Room, RoomType


UPDATES = [
    {
        "name": "Deluxe",
        "data": {
            "description": "Large room with sea-facing balcony.",
            "base_price": 1700000,
            "capacity": 3,
            "bed_count": 1,
            "amenities": "WiFi, TV, AC, Minibar, Balcony",
            "image": "https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=600&q=80",
        },
        "rooms": ["201", "202"],
        "floor": 2,
    },
    {
        "name": "Suite",
        "data": {
            "description": "Premium suite with lounge and city view.",
            "base_price": 2800000,
            "capacity": 2,
            "bed_count": 1,
            "amenities": "WiFi, TV, AC, Minibar, Jacuzzi",
            "image": "https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?auto=format&fit=crop&w=600&q=80",
        },
        "rooms": ["404"],
        "floor": 4,
    },
]


def main():
    for item in UPDATES:
        room_type, created = RoomType.objects.update_or_create(
            name=item["name"],
            defaults={"name": item["name"], **item["data"]},
        )
        action = "Created" if created else "Updated"
        print(f"{action} room type: {room_type.name}")

        for room_number in item["rooms"]:
            room, room_created = Room.objects.update_or_create(
                room_number=room_number,
                defaults={
                    "room_type": room_type,
                    "floor": item["floor"],
                    "status": "available",
                },
            )
            room_action = "Created" if room_created else "Updated"
            print(f"{room_action} room: {room.room_number}")


if __name__ == "__main__":
    main()
=======
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KIEMTHU.settings')
django.setup()

from hotel.models import Room

# Cập nhật phòng Apartment thành Twin Room
apartment = Room.objects.filter(name='Apartment').first()
if apartment:
    apartment.room_type = 'Twin'
    apartment.name = 'Twin Room'
    apartment.description = 'Phòng Twin Room có 2 giường đơn, rộng rãi và thoáng mát. Phù hợp cho khách đi hai người hoặc gia đình nhỏ.'
    apartment.capacity = 2
    apartment.price = 1500000
    apartment.save()
    print(f"✅ Cập nhật phòng thành công: {apartment.name} - {apartment.room_type} ({apartment.price:,} VND)")

# Thêm phòng Double Room mới
if not Room.objects.filter(room_type='Double').exists():
    new_room = Room.objects.create(
        name='Double Room',
        room_type='Double',
        price=1400000,
        description='Phòng Double Room có 1 giường đôi rộng, tiện nghi hiện đại. Lý tưởng cho các cặp vợ chồng hoặc những khách muốn giường lớn.',
        capacity=2,
        image='https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400'
    )
    print(f"✅ Thêm phòng mới: {new_room.name} - {new_room.room_type}")

# Thêm phòng Penthouse mới
if not Room.objects.filter(room_type='Penthouse').exists():
    penthouse = Room.objects.create(
        name='Penthouse Luxury',
        room_type='Penthouse',
        price=5000000,
        description='Penthouse sang trọng với tầm nhìn toàn cảnh, 2 phòng ngủ, phòng khách rộng và ban công riêng. Dịch vụ 5 sao.',
        capacity=4,
        image='https://images.unsplash.com/photo-1595576508898-c5c45f1d3843?w=400'
    )
    print(f"✅ Thêm phòng mới: {penthouse.name} - {penthouse.room_type}")

print("\n📋 Danh sách phòng hiện tại:")
for room in Room.objects.all():
    print(f"  - {room.name} ({room.room_type}): {room.price:,} VND, {room.capacity} người")

>>>>>>> be15ac174ec3f04303fa614df98f2bb4f6e9f869
