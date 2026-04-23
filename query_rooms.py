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
