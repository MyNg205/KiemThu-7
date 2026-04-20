import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KIEMTHU.settings')
import django
django.setup()

from django.test import Client
from hotel.models import Room

# Test 1: GET /book/ (form booking không có phòng pre-select)
print('Test 1: GET /book/ - Book without pre-selected room')
client = Client()
login_result = client.login(username='testuser', password='testuser123')
print(f'  Login result: {login_result}')
response = client.get('/book/')
print(f'  Status: {response.status_code}')
print(f'  Has context: {response.context is not None}')
if response.context:
    print(f'  Has selected_room: {"selected_room" in response.context}')
    print(f'  Has selected_room_type: {"selected_room_type" in response.context}')
    if 'selected_room' in response.context:
        print(f'    selected_room value: {response.context["selected_room"]}')
    if 'selected_room_type' in response.context:
        print(f'    selected_room_type value: {response.context["selected_room_type"]}')
    # Check HTML content
    if 'selected_room' not in response.context or response.context['selected_room'] is None:
        print('  ✓ No room pre-selected (correct)')
    else:
        print('  ✗ Room is pre-selected (should be None)')

# Test 2: GET /book/1/ (form booking có phòng pre-select)
print('\nTest 2: GET /book/1/ - Book with pre-selected room')
response = client.get('/book/1/')
print(f'  Status: {response.status_code}')
print(f'  Has context: {response.context is not None}')
if response.context:
    print(f'  Has selected_room: {"selected_room" in response.context}')
    print(f'  Has selected_room_type: {"selected_room_type" in response.context}')
    if 'selected_room' in response.context:
        room = response.context['selected_room']
        if room:
            print(f'    ✓ selected_room: Room #{room.room_number} (ID: {room.id})')
        else:
            print(f'    ✗ selected_room is None')
    if 'selected_room_type' in response.context:
        rt = response.context['selected_room_type']
        if rt:
            print(f'    ✓ selected_room_type: {rt.name} (ID: {rt.id})')
        else:
            print(f'    ✗ selected_room_type is None')

# Test 3: Check rooms availability
print('\nTest 3: Available rooms')
rooms = Room.objects.filter(status='available')
print(f'  Total available rooms: {len(rooms)}')
for room in rooms[:3]:
    print(f'    - Room {room.id}: {room.room_number} ({room.room_type.name})')




