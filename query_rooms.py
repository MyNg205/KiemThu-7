<<<<<<< HEAD
from _script_setup import setup

setup()

from hotel.models import Room, RoomType


def main():
    print("Room types:")
    for room_type in RoomType.objects.all():
        print(f"- {room_type.name}: {room_type.base_price}")

    print("\nRooms:")
    for room in Room.objects.select_related("room_type").all():
        print(f"- {room.room_number}: {room.room_type.name} ({room.status})")


if __name__ == "__main__":
    main()
=======
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KIEMTHU.settings')
import django
django.setup()
from hotel.models import RoomType, Room
print('Loại phòng hiện tại:')
for rt in RoomType.objects.all():
    print(rt)
print('\nPhòng hiện tại:')
for r in Room.objects.all():
    print(r)
>>>>>>> be15ac174ec3f04303fa614df98f2bb4f6e9f869
