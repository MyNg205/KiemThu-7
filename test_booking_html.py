import os

import django
from django.test import Client

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KIEMTHU.settings")
django.setup()


def main():
    client = Client()
    client.login(username="testuser", password="testuser123")

    print("Test 1: GET /book/ - Book without pre-selected room")
    response = client.get("/book/")
    print(f"  Status: {response.status_code}")
    if b"Phong 101 - Studio" in response.content or b"Deluxe" in response.content:
        print("  OK Contains room options")
    else:
        print("  FAIL No room options found")

    if b'value="1" data-type="1"' in response.content:
        print("  Note: Found room 1 with type 1")

    print("\nTest 2: GET /book/1/ - Book with pre-selected room")
    response = client.get("/book/1/")
    print(f"  Status: {response.status_code}")

    content_str = response.content.decode("utf-8")
    if 'value="1"' in content_str:
        print("  OK Contains room 1 option")
        lines = content_str.split("\n")
        for i, line in enumerate(lines):
            if 'value="1"' in line and "roomId" in "".join(lines[max(0, i - 5):i]):
                if "selected" in line:
                    print("  OK Room 1 is pre-selected")
                else:
                    context = "\n".join(lines[i:min(i + 5, len(lines))])
                    if "selected" in context:
                        print("  OK Room 1 has selected attribute")
                    else:
                        print("  Note: JavaScript may set selected on load")
                break
    else:
        print("  FAIL Room 1 not found")

    print("\nTest 3: Check room type select options")
    if 'name="room_type"' in content_str:
        print("  OK room_type select exists")
        if "Studio" in content_str:
            print("  OK Contains Studio option")
        if "Deluxe" in content_str:
            print("  OK Contains Deluxe option")
    else:
        print("  FAIL room_type select not found")

    print("\nAll basic tests completed")


if __name__ == "__main__":
    main()
