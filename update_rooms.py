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

