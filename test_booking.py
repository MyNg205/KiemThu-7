import os

import django
from django.test import Client

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KIEMTHU.settings")
django.setup()

from hotel.models import Room


def main():
    client = Client()

    print("Test 1: GET /book/ - Book without pre-selected room")
    login_result = client.login(username="testuser", password="testuser123")
    print(f"  Login result: {login_result}")
    response = client.get("/book/")
    print(f"  Status: {response.status_code}")
    print(f"  Has context: {response.context is not None}")
    if response.context:
        print(f"  Has selected_room: {'selected_room' in response.context}")
        print(f"  Has selected_room_type: {'selected_room_type' in response.context}")
        if "selected_room" in response.context:
            print(f"    selected_room value: {response.context['selected_room']}")
        if "selected_room_type" in response.context:
            print(f"    selected_room_type value: {response.context['selected_room_type']}")
        if "selected_room" not in response.context or response.context["selected_room"] is None:
            print("  OK No room pre-selected")
        else:
            print("  FAIL Room is pre-selected")

    print("\nTest 2: GET /book/1/ - Book with pre-selected room")
    response = client.get("/book/1/")
    print(f"  Status: {response.status_code}")
    print(f"  Has context: {response.context is not None}")
    if response.context:
        print(f"  Has selected_room: {'selected_room' in response.context}")
        print(f"  Has selected_room_type: {'selected_room_type' in response.context}")
        if "selected_room" in response.context:
            room = response.context["selected_room"]
            if room:
                print(f"    OK selected_room: Room #{room.room_number} (ID: {room.id})")
            else:
                print("    FAIL selected_room is None")
        if "selected_room_type" in response.context:
            room_type = response.context["selected_room_type"]
            if room_type:
                print(f"    OK selected_room_type: {room_type.name} (ID: {room_type.id})")
            else:
                print("    FAIL selected_room_type is None")

    print("\nTest 3: Available rooms")
    rooms = Room.objects.filter(status="available")
    print(f"  Total available rooms: {len(rooms)}")
    for room in rooms[:3]:
        print(f"    - Room {room.id}: {room.room_number} ({room.room_type.name})")


if __name__ == "__main__":
    main()
