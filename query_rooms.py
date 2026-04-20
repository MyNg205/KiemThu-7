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
