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
