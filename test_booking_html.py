import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KIEMTHU.settings')
import django
django.setup()

from django.test import Client

client = Client()
client.login(username='testuser', password='testuser123')

# Test 1: /book/
print('Test 1: GET /book/ - Book without pre-selected room')
response = client.get('/book/')
print(f'  Status: {response.status_code}')
if b'Phong 101 - Studio' in response.content or b'Deluxe' in response.content:
    print('  ✓ Contains room options')
else:
    print('  ✗ No room options found')

# Check for selected attribute on room 1
if b'value="1" data-type="1"' in response.content:
    print('  Note: Found room 1 with type 1')

# Test 2: /book/1/
print('\nTest 2: GET /book/1/ - Book with pre-selected room')
response = client.get('/book/1/')
print(f'  Status: {response.status_code}')

# Find the select element and check if room 1 is selected
content_str = response.content.decode('utf-8')
if 'value="1"' in content_str:
    print('  ✓ Contains room 1 option')
    # Find the specific line with room 1
    lines = content_str.split('\n')
    for i, line in enumerate(lines):
        if 'value="1"' in line and 'roomId' in ''.join(lines[max(0,i-5):i]):
            if 'selected' in line:
                print('  ✓ Room 1 is pre-selected (correct)')
            else:
                # Check next few lines
                context = '\n'.join(lines[i:min(i+5, len(lines))])
                if 'selected' in context:
                    print('  ✓ Room 1 has selected attribute')
                else:
                    print('  Note: Need to check if JavaScript sets selected on load')
            break
else:
    print('  ✗ Room 1 not found')

# Test 3: Check if room_type select has options
print('\nTest 3: Check room type select options')
if 'name="room_type"' in content_str:
    print('  ✓ room_type select exists')
    # Count options
    if 'Studio' in content_str:
        print('  ✓ Contains Studio option')
    if 'Deluxe' in content_str:
        print('  ✓ Contains Deluxe option')
else:
    print('  ✗ room_type select not found')

print('\nAll basic tests completed!')

